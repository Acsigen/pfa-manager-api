package routes

import (
	"net/http"
	"strconv"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/gin-gonic/gin"
)

// Display the client list
func get_client_list(context *gin.Context) {
	clients, err := models.Get_client_list()
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch clients."})
		return
	}
	context.JSON(http.StatusOK, clients)
}

// Get a client based on ID path parameter
func get_client(context *gin.Context) {
	// Retrieve the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}
	client, err := models.GetEventById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client."})
		return
	}

	context.JSON(http.StatusOK, client)
}

func create_client(context *gin.Context) {
	var client models.Client

	err := context.ShouldBindJSON(&client)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	client.ID = 1
	client.UserID = 1

	err = client.Add()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not add clients."})
		return
	}

	context.JSON(http.StatusCreated, gin.H{"message": "Client created", "client": client})
}

func update_client(context *gin.Context) {
	// Retrieve the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	_, err = models.GetEventById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client."})
		return
	}

	var updatedClient models.Client
	err = context.ShouldBindJSON(&updatedClient)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse client data."})
	}

	updatedClient.ID = client_id

	updatedClient.UserID = 1

	err = updatedClient.Update()
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not update client."})
		return
	}

	context.JSON(http.StatusOK, gin.H{"message": "Client updated"})
}
