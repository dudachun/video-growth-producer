import { Audio } from "@remotion/media";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

type Beat = {
  startSec: number;
  endSec: number;
  title: string;
  subtitle?: string;
  layout: "hook" | "wrong-right" | "steps" | "cta";
  bullets?: string[];
};

const beats: Beat[] = [
  {
    startSec: 0,
    endSec: 5,
    layout: "wrong-right",
    title: "Show the subject immediately",
    subtitle: "Do not waste the first 2 seconds.",
    bullets: ["wrong way", "right way"],
  },
  {
    startSec: 5,
    endSec: 20,
    layout: "steps",
    title: "Make the example concrete",
    bullets: ["scene", "action", "result"],
  },
  {
    startSec: 20,
    endSec: 38,
    layout: "steps",
    title: "Deliver useful density",
    bullets: ["proof", "workflow", "takeaway"],
  },
  {
    startSec: 38,
    endSec: 45,
    layout: "cta",
    title: "Follow for the next useful idea",
  },
];

const activeBeat = (sec: number) =>
  beats.find((beat) => sec >= beat.startSec && sec < beat.endSec) ?? beats[beats.length - 1];

export const VideoGrowthTemplate: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;
  const beat = activeBeat(sec);
  const local = frame - beat.startSec * fps;
  const enter = interpolate(local, [0, 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 18% 12%, rgba(249,115,22,0.28), transparent 32%), radial-gradient(circle at 86% 20%, rgba(56,189,248,0.28), transparent 34%), #06111f",
        color: "white",
        fontFamily: "Inter, Arial, sans-serif",
        padding: 56,
      }}
    >
      <div style={{ fontSize: 26, fontWeight: 900, color: "#fed7aa" }}>Video Growth Producer</div>
      <div
        style={{
          marginTop: 110,
          fontSize: 76,
          lineHeight: 1.02,
          fontWeight: 950,
          opacity: enter,
          transform: `translateY(${(1 - enter) * 40}px)`,
        }}
      >
        {beat.title}
      </div>
      {beat.subtitle && (
        <div
          style={{
            marginTop: 24,
            display: "inline-block",
            padding: "14px 20px",
            borderRadius: 18,
            background: "#fb923c",
            color: "#111827",
            fontSize: 34,
            fontWeight: 900,
          }}
        >
          {beat.subtitle}
        </div>
      )}
      <div style={{ marginTop: 80, display: "grid", gap: 18 }}>
        {(beat.bullets ?? []).map((item, index) => (
          <div
            key={item}
            style={{
              padding: 24,
              borderRadius: 24,
              background: index === 0 ? "rgba(239,68,68,0.7)" : "rgba(14,165,233,0.7)",
              fontSize: 38,
              fontWeight: 900,
              opacity: interpolate(local, [12 + index * 8, 26 + index * 8], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
            }}
          >
            {item}
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 56, right: 56, bottom: 58, height: 8, borderRadius: 999, background: "rgba(255,255,255,0.16)" }}>
        <div style={{ width: `${(sec / 45) * 100}%`, height: "100%", borderRadius: 999, background: "linear-gradient(90deg,#fb923c,#38bdf8)" }} />
      </div>
      {false && <Audio src={staticFile("voice.wav")} />}
    </AbsoluteFill>
  );
};

