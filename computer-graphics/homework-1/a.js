const canvas = $("#canvas")[0]
const ctx = canvas.getContext("2d")

const gear_width = 512
const gear_height = 512
const gear_image = new Image()
gear_image.src = "assets/gear2.png"

const x0 = (canvas.width - gear_width) / 2;
const y0 = (canvas.height - gear_height) / 2;

var t_current = Date.now()
var t_last = Date.now()

const angular_velocity = 2 * Math.PI / 5000;
var angle = 0

var a = 100

function draw()
{
    t_current = Date.now()
    const dt = t_current - t_last
    t_last = t_current

    angle += angular_velocity * dt;

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    ctx.save()

    ctx.translate(x0+gear_width/2, y0+gear_height/2);
    ctx.rotate(angle);
    ctx.translate(-x0-gear_width/2, -y0-gear_height/2);

    ctx.drawImage(gear_image, x0, y0, gear_width, gear_height);

    ctx.restore()
}

setInterval(draw, 10)