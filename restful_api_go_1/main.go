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
    
    // binding post body to newAlbum
    if err := c.BindJSON(&newAlbum); err !=nil {
        return
    }

    albums = append(albums, newAlbum)
    
    // response to the post req that man shall recieve 
    c.IndentedJSON(http.StatusCreated, newAlbum)
}

func main() {
    router := gin.Default()
    
    // like @app.route
    router.GET("/albums", getAlbums)
    router.POST("/albums", postAlbums)
    
    router.Run("localhost:8000")
}
