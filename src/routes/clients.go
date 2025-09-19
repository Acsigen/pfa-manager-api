package routes

import (
	"net/http"
	"strconv"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/gin-gonic/gin"
)

// Display the client list
func get_client_list(context *gin.Context) {
	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the clients list
	clients, err := models.GetClientList(userId)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch clients."})
		return
	}

	if clients == nil {
		context.JSON(http.StatusNotFound, gin.H{"message": "No clients to show"})
		return
	}
	// Return the clients if everything is ok
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

	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the client details from DB
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client."})
		return
	}

	// Only the owner can update data
	if client.UserID != userId {
		context.JSON(http.StatusUnauthorized, gin.H{"message": "You are not allowed to view this client"})
		return
	}

	// Display the client details with proper response code
	context.JSON(http.StatusOK, client)
}

// Add a client to the database route
func create_client(context *gin.Context) {
	// Initialise the client model
	var client models.Client

	// Check for the JSON body of the request to match the model
	err := context.ShouldBindJSON(&client)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	// Get the current user ID from the gin context which was set by the authentication middleware
	client.UserID = context.GetInt64("userId")

	// Add the client to the db
	err = client.Add()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not add clients."})
		return
	}

	// Display the added client as a confirmation
	context.JSON(http.StatusCreated, gin.H{"message": "Client created", "client": client})
}

func update_client(context *gin.Context) {
	// Retrieve the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the client based on ID from path parameter
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client."})
		return
	}

	// Only the owner can update data
	if client.UserID != userId {
		context.JSON(http.StatusUnauthorized, gin.H{"message": "You are not allowed to update this client"})
		return
	}

	// Initialise the updated client that should match the model
	var updatedClient models.Client
	err = context.ShouldBindJSON(&updatedClient)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse client data."})
	}

	// Set the proper client ID
	updatedClient.ID = client_id

	// Set the proper User ID
	updatedClient.UserID = userId

	// Update the client
	err = updatedClient.Update()
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not update client."})
		return
	}

	// Display a confirmation
	context.JSON(http.StatusOK, gin.H{"message": "Client updated"})
}

func delete_client(context *gin.Context) {
	// Retrieve the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the client based on ID from path parameter
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for deletion."})
		return
	}

	// Only the owner can delete data
	if client.UserID != userId {
		context.JSON(http.StatusUnauthorized, gin.H{"message": "You are not allowed to delete this client"})
		return
	}

	// Delete the client
	err = client.Delete(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not delete client."})
		return
	}

	// Display confirmation
	context.JSON(http.StatusOK, gin.H{"message": "Client deleted."})

}
