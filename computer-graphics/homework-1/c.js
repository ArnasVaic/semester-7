const canvas = $("#canvas")[0]
const ctx = canvas.getContext("2d")
const canvas_center = [canvas.width, canvas.height].map((x) => x / 2)

const clockScale = 1/4
const clockOutlinePng = new Image()
clockOutlinePng.src = "assets/clock.png" 

const secondHandlePhase = Math.PI + 2 * Math.PI * ((new Date).getSeconds()) / 60
const minuteHandlePhase = Math.PI + 2 * Math.PI * ((new Date).getMinutes()) / 60

function nextGearPosition(
  previousGearPosition,
  previousGearRadius,
  currentGearRadius,
  angle)
{
  let distance = previousGearRadius + currentGearRadius - 2 * PitchMinusInnerRadius
  let direction = [ Math.cos(angle), Math.sin(angle) ]
  return [
    previousGearPosition[0] + distance * direction[0],
    previousGearPosition[1] + distance * direction[1]
  ]
}

const gearSvgs = [8, 10, 60, 80].map(size => {
  let image = new Image()
  //image.src = `assets/involute_gear_80_to_${size}.svg`
  image.src = `assets/${size}-teeth-gear.svg`
  return image
})
// Unique values for different gear sizes
const gearScales = [0.475, 0.6, 3, 4] // By eye
const gearScaledRadii = gearSvgs.map((svg, i) => gearScales[i] * svg.width/2)

// Configurations for the entire scene
const PitchMinusInnerRadius = 7
// Ids into unique value arrays for each gear property
const sceneGearConfiguration = [ 2, 1, 3, 0 ] 
const sceneGearAngles = [0, 0, 0, 0]

function calculateGearPositions()
{
  let p1 = [ canvas_center[0] - 300, canvas_center[1] ]
  let p2 = nextGearPosition(p1, gearScaledRadii[sceneGearConfiguration[0]], gearScaledRadii[sceneGearConfiguration[1]], 0)
  let p3 = p2 // same position
  let p4 = nextGearPosition(p3, gearScaledRadii[sceneGearConfiguration[2]], gearScaledRadii[sceneGearConfiguration[3]], 0)
  return [p1, p2, p3, p4]
}
const sceneGearPositions = calculateGearPositions()

function calculateGearAngularVelocities()
{
  // T1 = 60 min
  const timeSpeedUp = 1
  let v1 = 2 * Math.PI / (1000 * 60 * 60)
  // T2 = 10min
  let v2 = 2 * Math.PI / (1000 * 60 * 10)
  let v3 = v2
  // T4 = 1min
  let v4 = 2 * Math.PI / (1000 * 60)
  // Alternating directions
  return [v1, -v2, -v3, v4].map(v => timeSpeedUp * v)
}

const sceneGearAngularVelocities = calculateGearAngularVelocities()

let t_current = Date.now()
let t_last = Date.now()

function drawClockOutline(center_position)
{
  ctx.save()
  ctx.drawImage(
    clockOutlinePng, 
    center_position[0] - clockScale * clockOutlinePng.width/2, 
    center_position[1] - clockScale * clockOutlinePng.height/2, 
    clockScale * clockOutlinePng.width, 
    clockScale * clockOutlinePng.height
  );
  ctx.restore();
}

function drawClockHand(position, color, angle, phase)
{
  let w = 2, h = 80
  let x = position[0]
  let y = position[1]

  ctx.save()

  ctx.translate(x, y)
  ctx.rotate(phase + angle)
  ctx.translate(-x, -y)
  ctx.beginPath()
  ctx.rect(x - w/2, y, w, h)
  let oldStyle = ctx.fillStyle;
  ctx.fillStyle = color;
  ctx.fill();
  ctx.fillStyle = oldStyle;
  ctx.closePath()
  ctx.restore()
}

function draw_gear(center_position, radius, angle, img)
{
  let x = center_position[0], y = center_position[1]
  ctx.save()
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.translate(-x, -y);
  ctx.drawImage(img, x - radius, y - radius, 2 * radius, 2 * radius);
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

function draw_gear_debug_info(
  center_position, 
  radius,
  pitch_radius_ratio,
  outside_radius_ratio)
{
  draw_circle(center_position, pitch_radius_ratio * radius, null, "#00ff00");
  draw_circle(center_position, outside_radius_ratio * radius, null, "#00ffff");
}

function draw()
{
  t_current = Date.now()
  const dt = t_current - t_last
  t_last = t_current

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  for(let i = 0; i < sceneGearPositions.length; ++i)
  {
    sceneGearAngles[i] += dt * sceneGearAngularVelocities[i]
    const gearId = sceneGearConfiguration[i]

    let position = sceneGearPositions[i]

    draw_gear(position, gearScaledRadii[gearId], sceneGearAngles[i], gearSvgs[gearId]);
  }  

  // Minute hand
  drawClockOutline(sceneGearPositions[0])
  drawClockHand(sceneGearPositions[0], '#000000', sceneGearAngles[0], minuteHandlePhase)

  // Second hand
  drawClockOutline(sceneGearPositions[3])
  drawClockHand(sceneGearPositions[3], '#ff0000', sceneGearAngles[3], secondHandlePhase)
}

setInterval(draw, 10)