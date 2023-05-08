# Distributed Systems Miniproject 2. Online Book Store

This project implements a simple book store application using the replication chain model. The application consists of a client, a server and a number of data stores. 

## Client
The client is a simple command line interface that allows the user to interact with the server. 

Available commands are:
* Local-store-ps: creates data store processes (nodes of the chain)
* Create-chain: Creates a chain of nodes
* List-chain: Shows the chain of nodes
* Write-operation: Write a new book to the chain
* List-books: Shows all books available in the store
* Read-operation: Reads a book from the chain
* Data-status: Shows the status of the books in the chain
* Remove-head: Removes the head of the chain
* Restore-head: Restores the head of the chain

## Server
Server is implemented according to a gRPC protocol. It receives requests from the client and responds accordingly.

## Data stores
Data stores are processes that store the books. They are connected into a chain after calling a `Create-chain` command on the client.
Each data store has links to its previous and next data stores, and to the head.

When a write operation is called, a new book is added to the head and an update is propagated along the chain from data store to data store.

Read operation can retrieve a book from any data store.