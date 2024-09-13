const canvas = $("#canvas")[0]
const ctx = canvas.getContext("2d")

const gear_count = 2
const gear_sizes = [512, 256]
const gear_radii = gear_sizes.map(x => x / 2)
const gear_placement_angles = [0, 60]

const gear_image = new Image()
gear_image.src = "assets/gear2.png"

let t_current = Date.now()
let t_last = Date.now()

const inside_radius_ratio = 206 / 256;
const pitch_radius_ratio = (1 + inside_radius_ratio) / 2;
const angular_velocity = 2 * Math.PI / 5000
let angle = 0

function draw_gear(p, r, a)
{
  ctx.save()
  ctx.translate(p[0] + r, p[1] + r);
  ctx.rotate(a);
  ctx.translate(-(p[0] + r), -(p[1] + r));
  ctx.drawImage(gear_image, p[0], [1], 2 * r, 2 * r);
  ctx.restore();
}

function draw_circle(p, r, fill_color, outline_color)
{
  ctx.save()
  ctx.beginPath();
  ctx.arc(p[0], p[1], r, 0, 2 * Math.PI, true);
  ctx.closePath();

  if(fill_color != null)
  {
    let oldStyle = ctx.fillStyle;
    ctx.fillStyle = fill_color;
    ctx.fill();
    ctx.fillStyle = oldStyle;
  }
  if(outline_color != null)
  {
    let oldStyle = ctx.strokeStyle;
    ctx.strokeStyle = outline_color;
    ctx.stroke();
    ctx.strokeStyle = oldStyle;
  }
  ctx.restore();
}

function draw_gear_debug_info(p, r)
{
  draw_circle(p, inside_radius_ratio * r, "#ff0000", null);
  draw_circle(p, pitch_radius_ratio * r, null, "#00ff00");
  draw_circle(p, r, null, "#0000ff");
}

function draw()
{
  t_current = Date.now()
  const dt = t_current - t_last
  t_last = t_current

  angle += angular_velocity * dt

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  ctx.save()

  let p_prev = [0, 0]
  for(let i = 0; i < gear_count; ++i)
  {
    let p
    let r = gear_radii[i]
    if (i == 0) {
      // First gear is always on center
      p = [canvas.width, canvas.height].map((x) => x / 2);
      p_prev = p
    } else {
      // Calculate next pos (pitch radii need to match)

      // Previous pitch radius + current pitch radius
      const dist = pitch_radius_ratio * (r + gear_radii[i - 1]);
      //
      let theta = gear_placement_angles[i];
      p = [p_prev + dist ]
      
    }


    draw_gear(p, r, angle);
    draw_gear_debug_info(p, r)
  }

  ctx.restore()
}

setInterval(draw, 10)