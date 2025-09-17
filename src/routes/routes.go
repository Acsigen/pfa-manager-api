package routes

import (
	"github.com/Acsigen/pfa-manager-api/middlewares"
	"github.com/gin-gonic/gin"
)

// Function to register routs
func RegisterRoutes(server *gin.Engine) {
	// Classic way of adding mdidlewares
	// // clients path listener
	// server.GET("/clients", middlewares.Authenticate, get_client_list)
	// // retrieve clients by id
	// server.GET("/clients/:id", middlewares.Authenticate, get_client)
	// // Add new client handler
	// server.POST("/clients", middlewares.Authenticate, create_client)
	// // Update client
	// server.PUT("/clients/:id", middlewares.Authenticate, update_client)
	// // Delete client
	// server.DELETE("/clients/:id", middlewares.Authenticate, delete_client)

	// Group clients requests and protect all of them with the authentication method
	authenticated := server.Group("/")
	authenticated.Use(middlewares.Authenticate)
	// clients path listener
	authenticated.GET("/clients", get_client_list)
	// retrieve clients by id
	authenticated.GET("/clients/:id", get_client)
	// Add new client handler
	authenticated.POST("/clients", create_client)
	// Update client
	authenticated.PUT("/clients/:id", update_client)
	// Delete client
	authenticated.DELETE("/clients/:id", delete_client)

	// Add contracts
	authenticated.POST("/clients/:id/contracts", add_contract)

	// Register a new user
	server.POST("/signup", signup)
	// Login to get the JWT Token
	server.POST("/login", login)
}
