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
}
