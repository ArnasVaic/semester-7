const canvas = $("#canvas")[0];
const ctx = canvas.getContext("2d");

ctx.font = "24px serif";

const W = canvas.width
const H = canvas.height

const I_FIGURE_MASK = [
  [1, 0, 0, 1],
  [1, 1, 1, 1],
  [0, 0, 1, 1],
  [0, 0, 1, 0],
]

const V_FIGURE_MASK = [
  [0, 0, 1, 0],
  [0, 0, 1, 1],
  [1, 1, 1, 1],
  [1, 0, 0, 1],
]

const H_FIGURE_MASK = [
  [1, 0, 0, 1],
  [1, 1, 1, 1],
  [1, 1, 0, 0],
  [0, 1, 0, 0],
]

const VH_FIGURE_MASK = [
  [0, 1, 0, 0],
  [1, 1, 0, 0],
  [1, 1, 1, 1],
  [1, 0, 0, 1],
]

// each fractal is basically copy base shape n times 
// and give each shape unique affine transforms (scale, translate, rotate)
const FRACTAL_CONFIG = [
  {
    color: '#880000',
    v_flip: false,
    h_flip: true,
    scale: [0.25, 0.25],
    offset: [-0.25, 0.25],
    rotate: Math.PI/2,
  },
  // {
  //   color: '#008800',
  //   flip: false,
  //   scale: [0.5, 0.5],
  //   offset: [-0.25, -0.25],
  //   rotate: -Math.PI,
  // },
  // {
  //   color: '#000088',
  //   flip: true,
  //   scale: [0.5, 0.5],
  //   offset: [0.25, 0.25],
  //   rotate: 0,
  // },
  // {
  //   color: '#880088',
  //   flip: false,
  //   scale: [0.5, 0.5],
  //   offset: [0.25, -0.25],
  //   rotate: Math.PI/2,
  // },
];

function circle_indicator(x, y, color)
{
  ctx.beginPath()
  ctx.arc(x, y, 8, 0, 2 * Math.PI, true)
  ctx.closePath()
  const oldFillStyle = ctx.fillStyle
  ctx.fillStyle = color
  ctx.fill()
  ctx.fillStyle = oldFillStyle
}

let draw_index = 0

function is_on_the_side(angle)
{
  return (Math.trunc(180 * Math.abs(angle) / Math.PI) / 90) % 2 == 1
}

function draw_fractal_recursive(step, x, y, scale_x, scale_y, angle, v_flip, h_flip, color)
{
  if (0 == step)
  {
    draw_base_figure(x, y, scale_x * W, scale_y * H, angle, color, v_flip, h_flip)
    return
  }

  const laying = is_on_the_side(angle)
  // if the parent is flipped so should be the child
  // along the parent? axis
  FRACTAL_CONFIG.map(t => {
  
    const rel_dx = scale_x * W * t.offset[0]
    const rel_dy = scale_y * H * t.offset[1]
    const abs_dx = rel_dx * Math.cos(angle) - rel_dy * Math.sin(angle)
    const abs_dy = rel_dx * Math.sin(angle) + rel_dy * Math.cos(angle)

    draw_fractal_recursive(
      step - 1, 
      x + (h_flip ? -1 : 1) * abs_dx, 
      y + (v_flip ? -1 : 1) * abs_dy, 
      scale_x * t.scale[0],
      scale_y * t.scale[1],
      angle + t.rotate,
      laying ? t.v_flip : t.h_flip,
      laying ? t.h_flip : t.v_flip,
      t.color
    );
  });
}

function draw_fractal(steps) {
  let a0 = Math.PI/2
  draw_fractal_recursive(steps, W/2, H/2, 1, 1, a0, 0, false, 'red')
}

function draw_base_figure(x, y, w, h, angle, color, v_flip, h_flip)
{
  ctx.save()

  ctx.translate(x, y)
  ctx.rotate(angle)
  
  const w_mini = w / 4
  const h_mini = h / 4

  ctx.beginPath()

  let mask = I_FIGURE_MASK
  if(v_flip && !h_flip) mask = V_FIGURE_MASK
  if(!v_flip && h_flip) mask = H_FIGURE_MASK
  if(v_flip && h_flip) mask = VH_FIGURE_MASK

  mask.map((row, i) => row.map((show, j) =>
    show && ctx.rect((j - 2) * w_mini, (i - 2) * h_mini, w_mini, h_mini)
  ))

  ctx.closePath()
  ctx.restore()
  
  const oldFillStyle = ctx.fillStyle
  ctx.fillStyle = color
  ctx.fill()
  ctx.fillStyle = oldFillStyle

  ctx.restore()

  const text_w = ctx.measureText(`${draw_index}`).width;
  ctx.fillText(`${Math.trunc(180 *angle / Math.PI)}`, x - text_w/2, y)

  draw_index = draw_index + 1
}

function draw_border()
{
  ctx.beginPath()
  ctx.lineTo(W, 0)
  ctx.lineTo(W, H);
  ctx.lineTo(0, H);
  ctx.lineTo(0, 0);
  ctx.closePath()
  ctx.stroke()
}

draw_border()

// draw_fractal(1)

// FRACTAL_CONFIG[0].color = '#ff0000'
// FRACTAL_CONFIG[1].color = '#00ff00'
// FRACTAL_CONFIG[2].color = '#0000ff'
// FRACTAL_CONFIG[3].color = '#ff00ff'

for(let i = 0; i < 3; ++i)
{
  draw_fractal(i)
}
