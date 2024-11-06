from fastapi import APIRouter, status


router = APIRouter(
    tags=["Health"]
)


@router.get("/healthy", status_code=status.HTTP_200_OK)
def health_check():
    """
    ***We make sure that the server is working properly.***
    """
    return {'status': 'Healthy'}
