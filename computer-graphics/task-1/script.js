const canvas = $("#canvas")[0];
const ctx = canvas.getContext("2d");

ctx.strokeStyle = '#00ff00'

// each fractar is basicly copy base shape n times 
// and give each shape unique affine transforms (scale, translate, rotate)
const FRACTAL_CONFIG = [
  {
    scale: 0.5,
    offset: [0, 0],
    rotate: 0,
  },
  {
    scale: 0.5,
    offset: [0.5, 0],
    rotate: 0,
  },
  {
    scale: 0.5,
    offset: [0, 0.5],
    rotate: 0,
  },
];

function transform(scale, offset, angle)
{
    const tx = canvas.width / 2
    const ty = canvas.height / 2
    const a = scale * Math.cos(angle)
    const b = scale * Math.sin(angle);
    const c = -scale * Math.sin(angle);
    const d = scale * Math.cos(angle);
    const e = tx * scale * Math.cos(angle) - ty * scale * Math.sin(angle) + canvas.width * offset[0]
    const f = tx * scale * Math.sin(angle) + ty * scale * Math.cos(angle) + canvas.width * offset[1]
    ctx.transform(a, b, c, d, e, f)
}

function draw_fractal(step)
{
    if (0 == step)
    {
        draw_base()
    }
    else
    {
        FRACTAL_CONFIG.map(t => {
            // we rotate around the center
            ctx.save()
            transform(t.scale, t.offset, t.angle)
            draw_fractal(step - 1);
            ctx.restore();
        });
    }
}

function draw_base()
{
    ctx.beginPath()
    ctx.lineTo(canvas.width, 0)
    ctx.lineTo(0, canvas.height);
    ctx.lineTo(0, 0);
    ctx.closePath()
    ctx.fill()
}

ctx.beginPath()
ctx.lineTo(canvas.width, 0)
ctx.lineTo(canvas.width, canvas.height);
ctx.lineTo(0, canvas.height);
ctx.lineTo(0, 0);
ctx.closePath()
ctx.stroke()

transform(0.25, [0.5, 0.5], Math.PI / 2)
draw_fractal(0)
