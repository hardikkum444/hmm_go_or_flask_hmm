// c *gin.Context is a pointer to a gin.Context object. This object contains information about the HTTP request and response

// when passing *gin.Context we are passing by ref which means we aint passing a copy we are passing the actual thing, any modifications will modify the actual thing

// The gin.Context object contains all the information about the current HTTP request and response.

package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

// creating a struct where man defines the structure of the db (in this case json)
type album struct {
    ID      string `json:"id"`
    Title   string `json:"title"`
    Artist  string `json:"artist"`
    Price   float64 `json:"price"`
}

// this is a slice or an array as man would call it
var albums = []album{
    {ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
    {ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
    {ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}

func getAlbums(c *gin.Context) {
    // response to the get req man shall recieve
    c.IndentedJSON(http.StatusOK, albums)
}

func postAlbums(c *gin.Context) {
    var newAlbum album
    
    // binding post body to newAlbum from the c (context) in json format
    if err := c.BindJSON(&newAlbum); err !=nil {
        return
    }

    albums = append(albums, newAlbum)
    
    // response to the post req that man shall recieve 
    c.IndentedJSON(http.StatusCreated, gin.H{"message": "item succesfully added"})
}

func getAlbumById(c *gin.Context) {
    id := c.Param("id")

    for _, a := range albums {
        if a.ID == id {
            c.IndentedJSON(http.StatusOK, a)
            return
        }
    }

    c.IndentedJSON(http.StatusNotFound, gin.H{"message":"not found error"})
}

func main() {
    router := gin.Default()
    
    // like @app.route
    router.GET("/albums", getAlbums)
    router.POST("/albums", postAlbums)
    router.GET("/albums/:id", getAlbumById)
    router.Run("localhost:8000")
}
