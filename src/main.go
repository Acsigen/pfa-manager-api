package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"

	"github.com/Acsigen/pfa-manager-api/database"
	"github.com/Acsigen/pfa-manager-api/routes"
)

// Display the welcome message for root path
func welcome_message(context *gin.Context) {
	context.JSON(http.StatusOK, gin.H{"message": "Welcome to PFA Manager API."})
}

func main() {
	var secretKey string = os.Getenv("PFA_SECRET_KEY")

	if secretKey == "" {
		panic("PFA_SECRET_KEY is missing")
	}
	// Init db
	database.InitDB()
	// Initialise the server
	server := gin.Default()
	// root path listener
	server.GET("/", welcome_message)

	// register routes from the routes package
	routes.RegisterRoutes(server)
	// Run the server
	server.Run("127.0.0.1:8000")
}
