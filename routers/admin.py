from fastapi import APIRouter, status
from services.kafka_services import topic_exists, create_topic, get_topics, delete_topics, update_topic, search_topic
from models.topic import Topic
from schemas.client import admin

router = APIRouter(
    prefix="/admin", 
    tags=["Admin"], 
    responses = {status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

# Listado de topics
@router.get("/", status_code=status.HTTP_200_OK)
async def kafka_list():
    #topics tiene la configuración de todo el cluster de Kafka
    return get_topics(admin)

# Obtener topic
@router.get("/topic/{name}", status_code=status.HTTP_200_OK)
async def kafka_list(name: str):
    if topic_exists(admin, name):
        return search_topic(admin, name)
    
    return {"message": f"Topic {name} does not exist."}

# Crear topic
@router.post("/created", status_code=status.HTTP_201_CREATED)
async def kafka_created_topic(topic: Topic):
    topic_name = topic.name
    max_msg_k = topic.max_bytes

    # Create topic if it doesn't exist
    if not topic_exists(admin, topic_name):
        create_topic(admin, topic_name, max_msg_k)
        return {"message": f"Topic {topic_name} created successfully! Max message size set to {max_msg_k} KB."}
    
    return {"message": f"Topic {topic_name} already exists."}

# Borrar topic
# Al usar el status HTTP_204_NO_CONTENT, no se devuelve ningún contenido en la respuesta.
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def kafka_delete_topic(topic: Topic):
    topic_name = topic.name

    if topic_exists(admin, topic_name):
        delete_topics(admin, topic_name)
        return {"message": f"Topic {topic_name} deleted successfully!"}
    
    return {"message": f"Topic {topic_name} does not exist."}

# Actualizar topic
@router.put("/update", status_code=status.HTTP_200_OK)
async def kafka_update_topic(topic: Topic):
    topic_name = topic.name
    max_msg_k = topic.max_bytes

    if topic_exists(admin, topic_name):
        update_topic(admin, topic_name, max_msg_k)
        return {"message": f"Max message size for topic {topic_name} updated to {max_msg_k} KB."}
    
    return {"message": f"Topic {topic_name} does not exist."}