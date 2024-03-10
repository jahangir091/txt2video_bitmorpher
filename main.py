import torch
import imageio
import uvicorn
from diffusers import TextToVideoZeroPipeline
import time
import uuid
import os


from fastapi import FastAPI, Body

# load stable diffusion model weights
model_id = "runwayml/stable-diffusion-v1-5"
# model_id = "sd-dreambooth-library/EpicMixVirtualRealismv6"
# model_id = "SG161222/RealVisXL_V4.0"


def get_img_path(directory_name):
    current_dir = '/tmp'
    video_directory = current_dir + '/.temp' + directory_name
    os.makedirs(video_directory, exist_ok=True)
    img_file_name = uuid.uuid4().hex[:20] + '.mp4'
    return video_directory + img_file_name


app = FastAPI()
app.pipe = TextToVideoZeroPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    cache_dir="models",
    return_cached_folder=True).to("cuda")


@app.post("/ai/api/v1/txt2video")
def read_root(
        prompt: str = Body("", title='prompt'),
        style_id: int = Body(1, title='style id'),
):
    start_time = time.time()

    # generate the video using our pipeline
    result = app.pipe(prompt=prompt).images
    result = [(r * 255).astype("uint8") for r in result]

    out_videos_directory_name = '/out_videos/'
    out_video_path = get_img_path(out_videos_directory_name)

    # save the resulting image
    imageio.mimsave(out_video_path, result, fps=8)

    return {
        "success": True,
        "message": "Returned output successfully",
        "server_process_time": time.time() - start_time,
        "output_media_url": '/media' + out_videos_directory_name + out_video_path.split('/')[-1]
    }


@app.get("/ai/api/v1/txt2video-server-test")
async def txt2video_server_test():

    return {
        "success": True,
        "message": "Server is OK."
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8009)




# rtx A5000