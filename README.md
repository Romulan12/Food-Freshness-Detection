# Food-Freshness-Detection

A simple Flask API to detect freshness in fruits. 
The CNN has been trained using fresh and stale images of the follwing items :
|   Fruits    |      
| ----------- | 
|   Banana    | 
|   Lemon     |
|   Lulo      |
|   Mango     | 
|   Orange    |
|  Strawberry |
|  Tamarillo  |
|   Tomato    | 

The dependencies are specified in ``` requirements.txt ```

## Steps for running the project
1. Build the docker: ``` docker build . -t freshness:1.0 ```
2. Running the container : ``` docker run -it --net=host -v /path_to_images_folder:/usr/src/app/data --name fresh -d freshness:1.0```

## Request body: 
```
{
    "docpath" : "/usr/src/app/data/your_image_name.jpg"
}
``` 

## To send the API request the url is: 
 http://0.0.0.0:8046/myapi/fruit-freshness-detection/
 





