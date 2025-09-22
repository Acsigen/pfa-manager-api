package routes

import (
	"net/http"
	"strconv"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/Acsigen/pfa-manager-api/utils"
	"github.com/gin-gonic/gin"
)

// Display the list
func get_invoice_list(context *gin.Context) {
	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the list
	invoices, err := models.GetInvoiceList(userId)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch invoices."})
		return
	}

	// Return the clients if everything is ok
	context.JSON(http.StatusOK, invoices)
}

// Add a new contract function
func add_invoice(context *gin.Context) {
	// Initialise the model
	var invoice models.Invoice

	// Get the client ID from the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	// Check if the JSON body matches the model
	err = context.ShouldBindJSON(&invoice)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	// Get the User ID from the context
	invoice.UserID = context.GetInt64("userId")

	// Set the proper client ID
	invoice.ClientID = client_id

	// Get the client based on ID from path parameter
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permission check"})
		return
	}

	// Only the owner can update data
	err = utils.CheckPermissions(invoice.UserID, client.UserID)

	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Add the contract to DB
	err = invoice.Add()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not invoice"})
		return
	}

	// Display confirmation message and contract contents
	context.JSON(http.StatusCreated, gin.H{"message": "Invoice created", "invoice": invoice})
}

// func get_contract(context *gin.Context) {
// 	// Retrieve the path parameter
// 	contract_id, err := strconv.ParseInt(context.Param("contract_id"), 10, 64)
// 	if err != nil {
// 		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid contract ID"})
// 		return
// 	}

// 	_, err = strconv.ParseInt(context.Param("id"), 10, 64)
// 	if err != nil {
// 		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
// 		return
// 	}

// 	// Get the user id from the authentication middleware
// 	userId := context.GetInt64("userId")

// 	// Get the contract details from DB
// 	contract, err := models.GetContractById(contract_id)

// 	if err != nil {
// 		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch contract.", "error": err.Error()})
// 		return
// 	}

// 	// Only the owner can update data
// 	err = utils.CheckPermissions(userId, contract.UserID)
// 	if err != nil {
// 		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
// 		return
// 	}

// 	// Display the contract details with proper response code
// 	context.JSON(http.StatusOK, contract)
// }

// func update_contract(context *gin.Context) {
// 	// Retrieve the path parameter
// 	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
// 	if err != nil {
// 		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
// 		return
// 	}
// 	contract_id, err := strconv.ParseInt(context.Param("contract_id"), 10, 64)
// 	if err != nil {
// 		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid contract ID"})
// 		return
// 	}

// 	// Get the user id from the authentication middleware
// 	userId := context.GetInt64("userId")

// 	// Get the client based on ID from path parameter
// 	client, err := models.GetClientById(client_id)

// 	if err != nil {
// 		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permission check"})
// 		return
// 	}

// 	// Only the owner can update data
// 	err = utils.CheckPermissions(userId, client.UserID)
// 	if err != nil {
// 		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
// 		return
// 	}

// 	// Initialise the updated client that should match the model
// 	var updatedContract models.Contract
// 	err = context.ShouldBindJSON(&updatedContract)

// 	if err != nil {
// 		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse contract data."})
// 	}

// 	// Set the proper contract ID
// 	updatedContract.ID = contract_id

// 	// Update the contract
// 	err = updatedContract.Update()
// 	if err != nil {
// 		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not update contract."})
// 		return
// 	}

// 	// Display a confirmation
// 	context.JSON(http.StatusOK, gin.H{"message": "Contract updated"})
// }

// func delete_contract(context *gin.Context) {
// 	// Retrieve the path parameter
// 	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
// 	if err != nil {
// 		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
// 		return
// 	}

// 	contract_id, err := strconv.ParseInt(context.Param("contract_id"), 10, 64)
// 	if err != nil {
// 		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid contract ID"})
// 		return
// 	}

// 	// Get the user id from the authentication middleware
// 	userId := context.GetInt64("userId")

// 	// Get the client based on ID from path parameter
// 	client, err := models.GetClientById(client_id)

// 	if err != nil {
// 		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permission check."})
// 		return
// 	}

// 	// Only the owner can update data
// 	err = utils.CheckPermissions(userId, client.UserID)
// 	if err != nil {
// 		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
// 		return
// 	}

// 	contract, err := models.GetContractById(contract_id)

// 	if err != nil {
// 		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch contract for deletion."})
// 		return
// 	}

// 	// Delete the client
// 	err = contract.Delete(contract_id)

// 	if err != nil {
// 		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not delete contract."})
// 		return
// 	}

// 	// Display confirmation
// 	context.JSON(http.StatusOK, gin.H{"message": "Contract deleted."})

// }
