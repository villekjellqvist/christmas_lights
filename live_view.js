var can = document.getElementById("live_view")
width = can.getAttribute("width")
height = can.getAttribute("height")
var ctx = can.getContext("2d");
ctx.fillStyle = "gray"
ctx.fillRect(0,0,width,height)



const nrpixels = 8

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

const socket = io.connect('http://127.0.0.1:5000');
socket.on("pixels", (colors) => {
    updatePixels(colors)
})

function updatePixels(colors) {
    for (let i = 0; i < nrpixels; i++) {
        pixels[i].color = colors[i]
        pixels[i].draw()
    }
}

setInterval("socket.emit(\"getPixels\")", 50)