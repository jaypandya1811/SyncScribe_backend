from fastapi import Request, status
from fastapi.responses import JSONResponse

async def user_already_exists_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def user_not_found_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def invalide_credentials_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def meeting_not_found_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def meeting_update_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def meeting_result_not_found_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )


async def meeting_result_update_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )
async def invalid_file_type_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def empty_file_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def file_size_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def file_extension_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def invalid_file_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def file_duration_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )

async def audio_converstion_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": str(exc),
        },
    )