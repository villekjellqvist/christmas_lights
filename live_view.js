var can = document.getElementById("live_view")
width = can.getAttribute("width")
height = can.getAttribute("height")
var ctx = can.getContext("2d");

const nrpixels = 50

class Pixel {
    constructor(x, y, size) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.color = "rgb(0, 0, 0)";
        this.draw = function () {
            ctx.fillStyle = this.color;
            ctx.clearRect(this.x, this.y, this.size, this.size);
            ctx.fillRect(this.x, this.y, this.size, this.size);
        };
    }
}

const pixels = []
pixelsWidth = Number((width - 20))
pixelSize = Number(pixelsWidth / nrpixels - 2)
for (let i = 0; i < nrpixels; i++) {
    x = Number(pixelsWidth * i / nrpixels) + 10
    y = Number(height / 2) - pixelSize / 2
    pixels[i] = new Pixel(x, y, pixelSize)
}

async function updatePixels() {
    const res = await fetch("http://127.0.0.1:5000/pixels")
    const palette = await res.json()

    for (let i = 0; i < nrpixels; i++) {
        pixels[i].color = palette[i]
        pixels[i].draw()
    }
}

setInterval(updatePixels, 20)

updatePixels()