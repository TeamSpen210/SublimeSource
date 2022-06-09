"""Generate completions for proxy strings."""
import json
from io import StringIO

PROXIES = []

def prox(name, *params):
	p = []
	for par in params:
		if isinstance(par, (list, tuple)):
			p.extend(par)
		else:
			p.append(par)
	PROXIES.append((name, p))

# Shorthands for these common ones.
res = "resultVar"
s1 = "srcVar1"
s2 = "srcVar2"

# Various combos that are repeated often.

# FunctionProxy
func = [s1, s2, res]
# Entity "getters"
scres = ["scale", res]
# AnimatedTexture
anim = [ "animatedtexturevar", "animatedtextureframenumvar", "animatedtextureframerate"]

prox("Add", func)
prox("Multiply", func)
prox("Subtract", func)
prox("Divide", func)
prox("Equals", s1, res)
prox("Abs", s1, res)
prox("Frac", s1, res)
prox("Int", s1, res)
prox("Clamp", "min", "max", s1, res)
prox("LessOrEqual", "lessEqualVar", "greaterVar", s1, s2)
prox("SelectFirstIfNonZero", func)
prox("WrapMinMax", s1, "minVal", "maxVal", res)
prox("Exponential", "minVal", "maxVal", s1, "offset", "scale", res)

# Number generation
prox("Sine", "sineperiod", "sinemin", "sinemax", "timeoffset", res)
prox("LinearRamp", "rate", "initialValue", res)
prox("CurrentTime", res)
prox("UniformNoise", "minVal", "maxVal", res)
prox("GaussianNoise", "mean", "halfWidth", "minVal", "maxVal", res)
prox("MatrixRotate", "axisVar", "angle", res)

# Entity reading
prox("Alpha")
prox("Cycle", "start", "end", "easein", "easeout", res)
prox("PlayerProximity", scres)
prox("PlayerTeamMatch", res)
prox("PlayerView", scres)
prox("PlayerSpeed", scres)
prox("PlayerPosition", scres)
prox("EntitySpeed", scres)
prox("EntityOrigin")
prox("EntityRandom", scres)
prox("Health", scres)
prox("IsNPC", scres)
prox("WorldDims")

# Texture control
prox("AnimatedTexture", anim)
prox("AnimatedEntityTexture", anim)
prox("AnimatedOffsetTexture", anim)
prox("AnimateSpecificTexture", anim, "onlyAnimateOnTexture")
prox("Pupil", "textureVar", "textureFrameNumVar", "pupilCloseRate", "pupilOpenRate")
prox("TextureTransform", "centerVar", "scaleVar", "rotateVar", "translateVar", res)
prox("TextureScroll", "textureScrollVar", "textureScrollRate", "textureScrollAngle")
prox("LampBeam")
prox("LampHalo")
prox("CustomSteamImageOnModel")

prox("MaterialModify")
prox("MaterialModifyAnimated", anim)
prox("WaterLOD")
prox("BreakableSurface")
prox("ConveyorScroll", "textureScrollVar")
prox("Camo")
prox("FleshInterior")
prox("HeliBlade")
prox("ParticleSphereProxy")
prox("PlayerLogo")
prox("Shadow")
prox("ShadowModel")
prox("ToggleTexture", "toggleTextureVar", "toggleTextureFrameNumVar", "toggleShouldWrap")

prox("Empty")
prox("Dummy")
prox("ConVar", "convar", res)

# HL2
prox("EntityOriginAlyx")
prox("Ep1IntroVortRefract")
prox("VortEmissive")
prox("Shield", "textureScrollVar", "textureScrollRate", "textureScrollAngle")

# TF2
prox("PlayerHealth", scres)
prox("PlayerDamageTime", scres)
prox("PlayerHealTime", scres)
prox("PlayerScore", scres)
prox("spy_invis")
prox("weapon_invis")
prox("vm_invis")
prox("invis")
prox("building_invis")
prox("CommunityWeapon", res)
prox("InvulnLevel", res)
prox("BurnLevel", res)
prox("YellowLevel", res)
prox("ModelGlowColor", res)
prox("ItemTintColor", res)
prox("BuildingRescueLevel", res)
prox("TeamTexture", res)
prox("AnimatedWeaponSheen", anim)
prox("WeaponSkin")
prox("ShieldFalloff")
prox("StatTrakIllum")
prox("StatTrakDigit")
prox("StatTrakIcon")
prox("StickybombGlowColor", res)
prox("SniperRifleCharge")
prox("Heartbeat")

# L4D2
prox("PlayerTeam", "team", res)
prox("BloodyHands", res)
prox("IT", res)
prox("BurnLevel", res)
prox("BBQLevel", res)

# ASW
prox("NightVisionSelfIllum", res)
prox("AlienSurfaceFX", "textureScrollVar")

# Portal
prox("PortalOpenAmount", res)
prox("PortalStatic", res)
prox("FizzlerVortex")
prox("WheatlyEyeGlow")
prox("Lightedmouth", res)
prox("LightedFloorButton", res)
prox("TractorBeam", res)

prox("TauCharge", res)
prox("SurvivalTeammate", res)

comp = []
buf = StringIO()

for name, params in PROXIES:
	buf.seek(0)
	buf.truncate()
	buf.write('{}\n'.format(name))
	buf.write('\t{\n')
	for i, param in enumerate(params, 1):
		buf.write('\t{} ${}\n'.format(param, i))
	buf.write('\t}')

	comp.append({'trigger': name + '\tProxy', 'contents': buf.getvalue()})

with open('vmt-proxies.sublime-completions', 'w') as f:
	json.dump({
	"scope": "meta.vmt.proxy-block",
	"completions": comp
	}, f, indent=2)
