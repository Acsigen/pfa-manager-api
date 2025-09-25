from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3  # For error handling
from ..database import db

class ActivityReport(BaseModel):
    id: int | None = None
    wo_id: int | None = None
    name: str
    date: str
    hours_amount: float
    user_id: int | None = None

    def add(self, wo_id: int, user_id: int):
        permitted_action: bool = check_permissions(
            item_id=wo_id, current_user_id=user_id, table_name="work_orders"
        )
        if permitted_action:
            query = "INSERT INTO activity_reports(wo_id, name, date, hours_amount, user_id) VALUES (?,?,?,?,?)"
            self.wo_id = wo_id
            self.user_id = user_id
            data: tuple = (
                self.wo_id,
                self.name,
                self.date,
                self.hours_amount,
                self.user_id,
            )
            try:
                res: sqlite3.Cursor = db.execute_query(query=query, params=data)
                self.id = res.lastrowid
                return self
            except sqlite3.Error as e:
                raise HTTPException(500, e.args[0])

    def update(self, ar_id: int, wo_id: int, user_id: int):
        permitted_action: bool = check_permissions(
            item_id=ar_id, current_user_id=user_id, table_name="activity_reports"
        )
        if permitted_action:
            query = "UPDATE activity_reports SET name = ?, date = ?, hours_amount = ? WHERE id == ? AND wo_id == ? AND user_id == ?"
            self.id = ar_id
            self.wo_id = wo_id
            self.user_id = user_id
            data = (
                self.name,
                self.date,
                self.hours_amount,
                self.id,
                self.wo_id,
                self.user_id,
            )
            try:
                _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                updated_activity_report: ActivityReport = show_activity_report(
                    activity_report_id=self.id, wo_id=self.wo_id, user_id=self.user_id
                )
                return updated_activity_report
            except sqlite3.Error as e:
                raise HTTPException(500, e.args[0])


def show_activity_report(wo_id: int, activity_report_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        item_id=activity_report_id,
        current_user_id=user_id,
        table_name="activity_reports",
    )
    if permitted_action:
        query = "SELECT * FROM activity_reports WHERE id == ? AND wo_id == ? AND user_id == ?"
        data = (activity_report_id, wo_id, user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            row: tuple = res.fetchone()
            if row:
                activity_report: ActivityReport = ActivityReport(
                    id=int(row[0]),
                    wo_id=row[1],
                    name=row[2],
                    date=row[3],
                    hours_amount=row[4],
                    user_id=row[5],
                )
                return activity_report
            else:
                raise HTTPException(404, "No such work order")
        except sqlite3.Error as e:
            raise HTTPException(500, e.args[0])


def list_activity_reports(wo_id: int, user_id: int):
    activity_report_list: list[ActivityReport] = []
    query = "SELECT * FROM activity_reports WHERE wo_id == ? AND user_id == ?"
    data: tuple = (wo_id, user_id)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        rows: list[tuple] = res.fetchall()
        for row in rows:
            activity_report: ActivityReport = ActivityReport(
                id=int(row[0]),
                wo_id=row[1],
                name=row[2],
                date=row[3],
                hours_amount=row[4],
                user_id=row[5],
            )
            activity_report_list.append(activity_report)
        return activity_report_list
    except sqlite3.OperationalError as e:
        raise HTTPException(500, e.args[0])


def delete_activity_report(wo_id: int, activity_report_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        item_id=activity_report_id,
        current_user_id=user_id,
        table_name="activity_reports",
    )
    if permitted_action:
        query = (
            "DELETE FROM activity_reports WHERE id == ? AND wo_id == ? AND user_id == ?"
        )
        data = (activity_report_id, wo_id, user_id)
        try:
            checkout_ar = show_activity_report(
                wo_id=wo_id, activity_report_id=activity_report_id, user_id=user_id
            )
            if type(checkout_ar) is ActivityReport:
                _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                return True
            else:
                raise HTTPException(404, "No such activity_report")
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])
