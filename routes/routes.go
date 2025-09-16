package routes

import "github.com/gin-gonic/gin"

// Function to register routs
func RegisterRoutes(server *gin.Engine) {
	// clients path listener
	server.GET("/clients", get_client_list)
	// retrieve clients by id
	server.GET("/clients/:id", get_client)
	// Add new client handler
	server.POST("/clients", create_client)
	// Update client
	server.PUT("/clients/:id", update_client)
	// Delete client
	server.DELETE("/clients/:id", delete_client)

	// Register a new user
	server.POST("/signup", signup)
	server.POST("/login", login)
}
