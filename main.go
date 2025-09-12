package main

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/Acsigen/pfa-manager-api/database"
	"github.com/Acsigen/pfa-manager-api/models"
)

// Display the welcome message for root path
func welcome_message(context *gin.Context) {
	context.JSON(http.StatusOK, gin.H{"message": "Welcome to PFA Manager API."})
}

// Display the client list
func get_client_list(context *gin.Context) {
	clients, err := models.Get_client_list()
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch clients."})
	}
	context.JSON(http.StatusOK, clients)
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
	}

	context.JSON(http.StatusCreated, gin.H{"message": "Client created", "client": client})
}

func main() {
	// Init db
	database.InitDB()
	// Initialise the server
	server := gin.Default()
	// root path listener
	server.GET("/", welcome_message)

	// clients path listener
	server.GET("/clients", get_client_list)

	server.POST("/clients", create_client)

	// Run the server
	server.Run("127.0.0.1:8000")
}
