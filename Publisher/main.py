from fastapi import FastAPI, HTTPException
from request_model import EmailRequestModel
from publisher_config import Publisher
from logger_config import logger

app = FastAPI()
publisher = Publisher()

@app.post("/publish")
async def publish_email_request(request: EmailRequestModel):
    logger.info(f"Received request: {request.dict()}")
    try:
        message = request.dict()
        publish_response = publisher.publish_message(message)
        logger.info(f"Response sent: {publish_response}")
        return {"message": "Published successfully", "publish_response": publish_response}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
    
    # how to kill process on particular port 
    # sudo netstat -tulnp | grep :8080
    # tcp   0   0 0.0.0.0:8080   0.0.0.0:*   LISTEN   12345/python
    # sudo kill -9 12345


