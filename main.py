import os
import requests
from concurrent.futures import ThreadPoolExecutor

def download_segment(variable):
    url = base_url.format(variable=variable)
    response = requests.get(url)

    if response.status_code == 200:
        output_file = os.path.join(output_dir, variable)
        with open(output_file, "wb") as f:
            f.write(response.content)
        return f"file '{output_file}'\n"
    else:
        print(f"Failed to download {variable} with status code {response.status_code}")
        return None

base_url = "https://hls2.videos.sproutvideo.com/f2cc9ed3f1a01b8c58cdfe59a1d8f215/46a8a0eafe9fec9292f7c8e47d54a12c/video/{variable}?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9obHMyLnZpZGVvcy5zcHJvdXR2aWRlby5jb20vZjJjYzllZDNmMWEwMWI4YzU4Y2RmZTU5YTFkOGYyMTUvNDZhOGEwZWFmZTlmZWM5MjkyZjdjOGU0N2Q1NGExMmMvKi50cz9zZXNzaW9uSUQ9ZjczNTVmY2EtYTk2NC00N2U0LWE2ZjItNDAwMzgxMzZiM2NiIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjg2MTUzMTQ4fX19XX0_&Signature=CNCiYIXR~tpAdATQqD9NClOt9TpBf~54jiTvMPPY0Y72IayQ-nuHLAX25Orr1mSQa4Jz6NKPMbEqp1ZjYP62RQUz9fVz6ZEKcUp1HE5QovX0V5F3r2y8QZKA7061jhHY09EOUcnh7IF61yNjXhxkf2v5G4Va96u~ZSvaqdDiNnAJ3Q5y4o4HMUTBWKHinhbricpJD9crc178fCj122izsP16pndimug~rcrgbOtyOB53cXr9yduvaztbZnXXpwAf9FEbwQQVuSNkD8-8aiDZlRtYY2x-x~sf59C9uNQ14ftJH2ZtqATLgTDxazZh4pwBMwPLel6bO940noax-gAv3Q__&Key-Pair-Id=APKAIB5DGCGAQJ4GGIUQ&sessionID=f7355fca-a964-47e4-a6f2-40038136b3cb"

output_dir = "downloaded_segments_4k"
os.makedirs(output_dir, exist_ok=True)

variables = [f"2160_{i:05d}.ts" for i in range(0, 676)]

with ThreadPoolExecutor() as executor:
    results = list(executor.map(download_segment, variables))

with open("concat_list.txt", "w") as concat_list:
    for result in results:
        if result is not None:
            concat_list.write(result)


# decrypt: ffmpeg -f concat -safe 0 -i concat_list.txt -c copy output.ts
# convert to MP4: ffmpeg -i input.ts -c:v libx264 -preset slow -crf 22 -:a aac -b:a 128k output.mp4
