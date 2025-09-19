package utils

import "errors"

func CheckPermissions(context_user_id int64, db_user_id int64) error {
	// Only the owner can perform action
	if context_user_id != db_user_id {
		return errors.New("you are not allowed to to perform this action")
	} else {
		return nil
	}
}
