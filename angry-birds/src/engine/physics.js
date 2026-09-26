import Matter from 'matter-js'

let engine = null
let render = null
let runner = null
let currentProjectile = null
let currentSling = null
let mouseConstraint = null

let slingX = 0
let slingY = 0

let damageTexts = []
let isWorldSettling = true;
let currentHpMultiplier = 1.0;

const CATEGORY_DEFAULT = 0x0001;
const CATEGORY_DRAGGABLE = 0x0002;

const ammoPhysicsData = {
    kayu: { density: 0.04, restitution: 0.4, color: '#b45309' },
    batu: { density: 0.1, restitution: 0.2, color: '#78716c' },
    besi: { density: 0.5, restitution: 0.05, color: '#94a3b8' }
}

const materialData = {
    kaca: { density: 0.02, restitution: 0.1, color: '#bae6fd', maxHp: 30 },
    kayu: { density: 0.04, restitution: 0.4, color: '#d97706', maxHp: 100 },
    batu: { density: 0.15, restitution: 0.2, color: '#57534e', maxHp: 400 }
}

const createBlock = (x, y, w, h, materialType) => {
    const mat = materialData[materialType] || materialData.kayu;
    const finalHp = mat.maxHp * currentHpMultiplier;

    return Matter.Bodies.rectangle(x, y, w, h, {
        label: `block_${materialType}`,
        density: mat.density, restitution: mat.restitution, render: { fillStyle: mat.color, opacity: 1.0 },
        collisionFilter: { category: CATEGORY_DEFAULT },
        plugin: { hp: finalHp, maxHp: finalHp }
    });
};

export const initPhysics = (containerElement, planetId, gravityValue, onScoreUpdate, onAmmoUsed) => {
    currentHpMultiplier = 1.0;
    if (planetId === '2') currentHpMultiplier = 1.5;
    if (planetId === '3') currentHpMultiplier = 2.5;

    if (engine) return

    const { Engine, Render, Runner, World, Bodies, Mouse, MouseConstraint, Constraint, Events, Composite } = Matter

    engine = Engine.create()
    engine.world.gravity.y = gravityValue

    isWorldSettling = true;
    setTimeout(() => { isWorldSettling = false; }, 2000);

    const width = window.innerWidth
    const height = window.innerHeight

    const isMobile = height < 600;
    const scale = isMobile ? 0.7 : 1.0;

    const floorY = height - (isMobile ? 80 : 100);

    slingX = width * 0.15;
    slingY = floorY - (100 * scale);

    const castleX = width * 0.80;
    const obstacleX = width * 0.50;

    render = Render.create({
        element: containerElement,
        engine: engine,
        options: { width, height, wireframes: false, background: 'transparent' }
    })

    const ground = Bodies.rectangle(width / 2, floorY + 100, width * 2, 200, {
        isStatic: true, label: 'ground', render: { fillStyle: '#1e293b' }, collisionFilter: { category: CATEGORY_DEFAULT }
    })

    currentProjectile = Bodies.circle(slingX, slingY, 20 * scale, {
        label: 'proyektil',
        density: ammoPhysicsData['kayu'].density,
        restitution: ammoPhysicsData['kayu'].restitution,
        render: { fillStyle: ammoPhysicsData['kayu'].color },
        collisionFilter: { category: CATEGORY_DRAGGABLE, mask: CATEGORY_DEFAULT }
    })

    currentSling = Constraint.create({
        pointA: { x: slingX, y: slingY },
        bodyB: currentProjectile,
        stiffness: 0.05, damping: 0.01,
        render: { visible: false }
    })

    const enemyTexture = 'data:image/svg+xml;utf8,<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="20" r="20" fill="%23ef4444"/><circle cx="12" cy="15" r="5" fill="white"/><circle cx="28" cy="15" r="5" fill="white"/><circle cx="12" cy="15" r="2" fill="black"/><circle cx="28" cy="15" r="2" fill="black"/><path d="M 12 28 Q 20 22 28 28" stroke="white" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'
    const enemyRadius = 20 * scale;

    const enemyMaxHp = 60 * currentHpMultiplier;
    const enemyOptions = {
        label: 'target', density: 0.02, restitution: 0.2,
        render: { sprite: { texture: enemyTexture, xScale: scale, yScale: scale }, opacity: 1.0 },
        collisionFilter: { category: CATEGORY_DEFAULT },
        plugin: { hp: enemyMaxHp, maxHp: enemyMaxHp }
    }

    const bw = 20 * scale;
    const bh = 80 * scale;

    const levelBodies = [
        Bodies.rectangle(obstacleX, floorY - (80*scale), 30*scale, 160*scale, { isStatic: true, render: { fillStyle: '#334155' }, collisionFilter: { category: CATEGORY_DEFAULT } }),
        createBlock(castleX - (100*scale), floorY - (bh/2), bw, bh, 'kayu'),
        createBlock(castleX, floorY - (bh/2), bw, bh, 'kaca'),
        createBlock(castleX + (100*scale), floorY - (bh/2), bw, bh, 'kayu'),
        Bodies.circle(castleX - (50*scale), floorY - enemyRadius, enemyRadius, enemyOptions),
        Bodies.circle(castleX + (50*scale), floorY - enemyRadius, enemyRadius, enemyOptions),
        createBlock(castleX, floorY - bh - (10*scale), 260*scale, 20*scale, 'batu'),
        createBlock(castleX - (60*scale), floorY - bh - (20*scale) - (bh/2), bw, bh, 'kayu'),
        createBlock(castleX + (60*scale), floorY - bh - (20*scale) - (bh/2), bw, bh, 'kayu'),
        Bodies.circle(castleX, floorY - bh - (20*scale) - enemyRadius, enemyRadius, enemyOptions),
        createBlock(castleX, floorY - (bh*2) - (30*scale), 180*scale, 20*scale, 'batu'),
        createBlock(castleX - (30*scale), floorY - (bh*2) - (40*scale) - (bh/2), bw, bh, 'kaca'),
        createBlock(castleX + (30*scale), floorY - (bh*2) - (40*scale) - (bh/2), bw, bh, 'kaca'),
        Bodies.circle(castleX, floorY - (bh*2) - (40*scale) - enemyRadius, enemyRadius, enemyOptions),
        createBlock(castleX, floorY - (bh*3) - (50*scale), 80*scale, 20*scale, 'kayu'),
    ]

    const mouse = Mouse.create(render.canvas)
    mouseConstraint = MouseConstraint.create(engine, {
        mouse: mouse,
        constraint: { stiffness: 0.1, render: { visible: false } },
        collisionFilter: { mask: CATEGORY_DRAGGABLE }
    })
    render.mouse = mouse

    render.canvas.addEventListener('contextmenu', (e) => { e.stopPropagation(); }, true);

    Events.on(engine, 'beforeUpdate', () => {
        if (mouseConstraint.mouse.button !== -1 && mouseConstraint.body === currentProjectile) {
            const maxDrag = 120 * scale;
            const dx = currentProjectile.position.x - slingX;
            const dy = currentProjectile.position.y - slingY;
            const dist = Math.sqrt(dx * dx + dy * dy);

            let newX = currentProjectile.position.x;
            let newY = currentProjectile.position.y;

            if (dist > maxDrag) {
                newX = slingX + (dx / dist) * maxDrag;
                newY = slingY + (dy / dist) * maxDrag;
            }

            const groundLimit = floorY - (22 * scale);
            if (newY > groundLimit) {
                newY = groundLimit;
            }

            if (newX !== currentProjectile.position.x || newY !== currentProjectile.position.y) {
                Matter.Body.setPosition(currentProjectile, { x: newX, y: newY });
            }
        }
    });

    Events.on(engine, 'collisionStart', (event) => {
        if (isWorldSettling) return;

        event.pairs.forEach((pair) => {
            const { bodyA, bodyB } = pair;
            const relativeSpeed = Math.abs(bodyA.speed - bodyB.speed);

            if (relativeSpeed < 1.5) return;

            const isProjectileInvolved = bodyA.label === 'proyektil' || bodyB.label === 'proyektil';
            const impactForce = (bodyA.mass + bodyB.mass) * relativeSpeed;
            const damageMultiplier = isProjectileInvolved ? 0.06 : 0.01;
            const damage = impactForce * damageMultiplier;

            const applyDamage = (body) => {
                if (body.plugin && body.plugin.hp !== undefined && !body.isDestroyed) {
                    body.plugin.hp -= damage;

                    if (body.label.startsWith('block_') || body.label === 'target') {
                        body.render.opacity = Math.max(0.3, body.plugin.hp / body.plugin.maxHp);
                    }

                    if (body.plugin.hp <= 0) {
                        body.isDestroyed = true;
                        let points = body.label === 'target' ? 1000 : 100;
                        let textMsg = body.label === 'target' ? 'CRITICAL!' : 'SMASH!';
                        let textColor = body.label === 'target' ? '#ef4444' : '#f59e0b';
                        damageTexts.push({ x: body.position.x, y: body.position.y - 20, text: textMsg, color: textColor, alpha: 1.0, life: 60 });
                        const reportedLabel = body.label === 'target' ? 'target' : 'block';

                        Composite.remove(engine.world, body);
                        if (onScoreUpdate) onScoreUpdate(points, reportedLabel);
                    }
                }
            };
            applyDamage(bodyA);
            applyDamage(bodyB);
        })
    })

    Events.on(mouseConstraint, 'enddrag', (event) => {
        if (event.body === currentProjectile) {
            currentProjectile.collisionFilter.category = CATEGORY_DEFAULT;
            setTimeout(() => {
                currentSling.bodyB = null;
                if (onAmmoUsed) onAmmoUsed();
            }, 50);
        }
    });

    Events.on(render, 'afterRender', () => {
        const ctx = render.context;
        const anchorX = currentSling.pointA.x;
        const anchorY = currentSling.pointA.y;

        ctx.beginPath();
        ctx.arc(anchorX, anchorY, 12 * scale, 0, 2 * Math.PI);
        ctx.fillStyle = 'rgba(56, 189, 248, 0.2)';
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#38bdf8';
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(anchorX, anchorY, 4 * scale, 0, 2 * Math.PI);
        ctx.fillStyle = '#bae6fd';
        ctx.fill();

        if (currentSling.bodyB === currentProjectile) {
            const startX = currentProjectile.position.x;
            const startY = currentProjectile.position.y;

            ctx.beginPath();
            ctx.moveTo(anchorX, anchorY);
            ctx.lineTo(startX, startY);
            ctx.strokeStyle = '#94a3b8';
            ctx.lineWidth = 4 * scale;
            ctx.stroke();

            if (mouseConstraint.mouse.button === 0 && mouseConstraint.body === currentProjectile) {
                const pullX = anchorX - startX;
                const pullY = anchorY - startY;

                ctx.beginPath();
                ctx.moveTo(anchorX, anchorY);
                ctx.lineTo(anchorX + (pullX * 3), anchorY + (pullY * 3));
                ctx.setLineDash([8, 8]);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
                ctx.lineWidth = 2 * scale;
                ctx.stroke();
                ctx.setLineDash([]);
            }
        }

        for (let i = damageTexts.length - 1; i >= 0; i--) {
            let dt = damageTexts[i];
            ctx.globalAlpha = dt.alpha;
            ctx.fillStyle = dt.color;
            ctx.font = `900 ${24 * scale}px 'Courier New', monospace`;
            ctx.textAlign = "center";
            ctx.strokeStyle = "rgba(0,0,0,0.8)";
            ctx.lineWidth = 4 * scale;
            ctx.strokeText(dt.text, dt.x, dt.y);
            ctx.fillText(dt.text, dt.x, dt.y);

            dt.y -= 1.5; dt.alpha -= 0.015; dt.life--;
            if (dt.life <= 0) damageTexts.splice(i, 1);
        }
        ctx.globalAlpha = 1.0;
    });

    World.add(engine.world, [ground, currentProjectile, currentSling, ...levelBodies, mouseConstraint])
    Render.run(render)
    runner = Runner.create()
    Runner.run(runner, engine)
}

export const reloadProjectile = (type) => {
    if (!engine) return
    const props = ammoPhysicsData[type] || ammoPhysicsData['kayu']

    const isMobile = window.innerHeight < 600;
    const scale = isMobile ? 0.7 : 1.0;

    if (currentProjectile && currentSling.bodyB === currentProjectile) {
        Matter.Composite.remove(engine.world, currentProjectile)
    }

    currentProjectile = Matter.Bodies.circle(slingX, slingY, 20 * scale, {
        label: 'proyektil',
        density: props.density,
        restitution: props.restitution,
        render: { fillStyle: props.color },
        collisionFilter: { category: CATEGORY_DRAGGABLE, mask: CATEGORY_DEFAULT }
    })

    currentSling.bodyB = currentProjectile
    Matter.World.add(engine.world, currentProjectile)
}

export const setAmmoEngine = (type) => {
    if (!engine || !currentProjectile) return
    if (currentSling.bodyB === currentProjectile) {
        reloadProjectile(type)
    }
}

export const destroyPhysics = () => {
    if (render) { Matter.Render.stop(render); render.canvas.remove(); render = null }
    if (runner) { Matter.Runner.stop(runner); runner = null }
    if (engine) { Matter.Events.off(engine); Matter.World.clear(engine.world); Matter.Engine.clear(engine); engine = null }
    mouseConstraint = null; damageTexts = []
}