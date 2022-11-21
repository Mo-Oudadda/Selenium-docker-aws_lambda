import uvicorn
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from mangum import Mangum
import sys
from tempfile import mkdtemp
from selenium import webdriver

app = FastAPI()


class Params(BaseModel):
    url: str 


@app.post("/")
def get_altitude(params: Params):
    
    url = params.url
=
    try:
        # -- driver options --
        options = webdriver.ChromeOptions()
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome("/opt/chromedriver",
                                  options=options)
        # -- open firefox driver for web crawling --

        driver.get(url)

        # Rest of code here
        result = 10
        driver.quit()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail=f'Could not navigate to URL. Details: {e}'
        )

    return {'url': url,
            'result': result,
            }


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
