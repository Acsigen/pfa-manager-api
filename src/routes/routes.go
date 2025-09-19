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
	// Clients
	authenticated.GET("/clients", get_client_list)
	authenticated.GET("/clients/:id", get_client)
	authenticated.POST("/clients", create_client)
	authenticated.PUT("/clients/:id", update_client)
	authenticated.DELETE("/clients/:id", delete_client)

	// Contracts
	authenticated.POST("/clients/:id/contracts", add_contract)
	authenticated.GET("/clients/:id/contracts", get_contract_list)
	authenticated.PUT("/clients/:id/contracts/:contract_id", update_contract)
	authenticated.GET("/clients/:id/contracts/:contract_id", get_contract)
	authenticated.DELETE("/clients/:id/contracts/:contract_id", delete_contract)

	// Work Orders
	authenticated.POST("/clients/:id/contracts/:contract_id/wo", add_wo)
	authenticated.GET("/clients/:id/contracts/:contract_id/wo", get_wo_list)
	authenticated.PUT("/clients/:id/contracts/:contract_id/wo/:wo_id", update_wo)
	authenticated.GET("/clients/:id/contracts/:contract_id/wo/:wo_id", get_wo)
	authenticated.DELETE("/clients/:id/contracts/:contract_id/wo/:wo_id", delete_wo)

	// Activity Reports
	// authenticated.POST("/clients/:id/contracts/:contract_id/wo/:wo_id", add_ar)
	// authenticated.GET("/clients/:id/contracts/:contract_id/wo", get_wo_list)
	// authenticated.PUT("/clients/:id/contracts/:contract_id/wo/:wo_id", update_wo)
	// authenticated.GET("/clients/:id/contracts/:contract_id/wo/:wo_id", get_wo)
	// authenticated.DELETE("/clients/:id/contracts/:contract_id/wo/:wo_id", delete_wo)

	// Register a new user
	server.POST("/signup", signup)
	// Login to get the JWT Token
	server.POST("/login", login)
}
