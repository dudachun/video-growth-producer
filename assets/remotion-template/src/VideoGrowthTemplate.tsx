import type { CSSProperties, FC, ReactNode } from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { episodeManifest } from "./episode_manifest";
import type { Caption, VisualBeat } from "./types";

const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
const ink = "#0f172a";
const blue = "#2563eb";
const cyan = "#38bdf8";
const yellow = episodeManifest.video.captionHighlightColor ?? "#ffd84d";

const activeBeat = (sec: number, beats: VisualBeat[]) =>
  beats.find((beat) => sec >= beat.startSec && sec < beat.endSec) ?? beats[beats.length - 1];

const activeCaption = (sec: number, captions: Caption[]) => {
  const ms = sec * 1000;
  return captions.find((caption) => ms >= caption.startMs && ms < caption.endMs) ?? captions[captions.length - 1];
};

const progress = (frame: number, fps: number, startSec: number, durationSec: number) =>
  interpolate(frame, [startSec * fps, (startSec + durationSec) * fps], [0, 1], {
    ...clamp,
    easing: easeOut,
  });

const beatOpacity = (frame: number, fps: number, beat: VisualBeat) => {
  const start = beat.startSec * fps;
  const end = beat.endSec * fps;
  const fadeIn = interpolate(frame, [start, start + 8], [0, 1], clamp);
  const fadeOut = interpolate(frame, [end - 8, end], [1, 0], clamp);
  return Math.min(fadeIn, fadeOut);
};

const sceneStyle = (frame: number, fps: number, beat: VisualBeat): CSSProperties => {
  const p = progress(frame, fps, beat.startSec, 0.55);
  return {
    opacity: beatOpacity(frame, fps, beat),
    transform: `translateY(${(1 - p) * 42}px) scale(${0.97 + p * 0.03})`,
  };
};

const splitHighlightedText = (text: string, terms: string[]) => {
  const cleanTerms = terms.filter(Boolean).sort((a, b) => b.length - a.length);
  if (!cleanTerms.length) return [text];
  const escaped = cleanTerms.map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const pattern = new RegExp(`(${escaped.join("|")})`, "g");
  return text.split(pattern).filter(Boolean);
};

const CaptionLine: FC<{ caption: Caption; terms: string[] }> = ({ caption, terms }) => (
  <div
    style={{
      position: "absolute",
      zIndex: 200,
      top: `${episodeManifest.video.captionTopPercent}%`,
      left: 70,
      right: 70,
      transform: "translateY(-50%)",
      textAlign: "center",
      fontFamily: '"Noto Serif SC", "Source Han Serif SC", "Microsoft YaHei", serif',
      fontWeight: 900,
      fontSize: 48,
      lineHeight: 1.22,
      color: "white",
      textShadow: "0 4px 12px rgba(0,0,0,0.95), 0 2px 4px rgba(0,0,0,0.9)",
      letterSpacing: 0,
    }}
  >
    {splitHighlightedText(caption.text, terms).map((part, index) => (
      <span key={`${part}-${index}`} style={{ color: terms.includes(part) ? yellow : "white" }}>
        {part}
      </span>
    ))}
  </div>
);

const Shell: FC<{ children: ReactNode }> = ({ children }) => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(circle at 12% 10%, rgba(56,189,248,0.22), transparent 24%), radial-gradient(circle at 90% 16%, rgba(250,204,21,0.16), transparent 22%), linear-gradient(180deg,#f8fbff,#edf6ff)",
      color: ink,
      overflow: "hidden",
      fontFamily: 'Inter, "Microsoft YaHei", "PingFang SC", Arial, sans-serif',
    }}
  >
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundImage:
          "linear-gradient(rgba(37,99,235,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(37,99,235,0.07) 1px, transparent 1px)",
        backgroundSize: "72px 72px",
      }}
    />
    {children}
  </AbsoluteFill>
);

const BrandBar: FC = () => (
  <div style={{ position: "absolute", zIndex: 100, top: 48, left: 56, right: 56, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
    <div style={{ fontSize: 26, fontWeight: 950, color: blue }}>{episodeManifest.seriesName ?? "Video Growth Producer"}</div>
    <div
      style={{
        padding: "10px 16px",
        borderRadius: 999,
        background: episodeManifest.mode === "strict" ? "#dcfce7" : "#fff7ed",
        color: episodeManifest.mode === "strict" ? "#166534" : "#c2410c",
        fontSize: 20,
        fontWeight: 900,
      }}
    >
      {episodeManifest.mode === "strict" ? "STRICT PUBLISH" : "REMOTION-ONLY PREVIEW"}
    </div>
  </div>
);

const AssetPanel: FC<{ beat: VisualBeat; frame: number; fps: number }> = ({ beat, frame, fps }) => {
  const asset = beat.asset ?? beat.imagegenAsset;
  const p = progress(frame, fps, beat.startSec + 0.2, 0.65);
  if (asset) {
    return (
      <div
        style={{
          ...card,
          height: 520,
          overflow: "hidden",
          transform: `scale(${0.96 + p * 0.04})`,
        }}
      >
        <Img src={staticFile(asset)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    );
  }

  return (
    <div style={{ ...card, height: 520, padding: 36, position: "relative", overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            beat.assetSource === "imagegen"
              ? "linear-gradient(135deg, rgba(14,165,233,0.18), rgba(250,204,21,0.2))"
              : "linear-gradient(135deg, rgba(37,99,235,0.16), rgba(255,255,255,0.1))",
        }}
      />
      <div style={{ position: "relative", display: "grid", gap: 18 }}>
        {(beat.bullets ?? ["visual asset", "motion cue", "proof"]).slice(0, 4).map((item, index) => {
          const itemP = progress(frame, fps, beat.startSec + 0.25 + index * 0.16, 0.35);
          return (
            <div
              key={item}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 16,
                padding: "20px 22px",
                borderRadius: 22,
                background: "rgba(255,255,255,0.88)",
                boxShadow: "0 16px 48px rgba(24,86,154,0.12)",
                fontSize: 30,
                fontWeight: 900,
                transform: `translateX(${(1 - itemP) * 40}px)`,
                opacity: itemP,
              }}
            >
              <span style={{ width: 18, height: 18, borderRadius: 999, background: index % 2 ? cyan : yellow }} />
              {item}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const card: CSSProperties = {
  borderRadius: 28,
  background: "rgba(255,255,255,0.94)",
  border: "1px solid rgba(37,99,235,0.16)",
  boxShadow: "0 28px 80px rgba(24,86,154,0.16)",
};

const TitleBlock: FC<{ beat: VisualBeat; frame: number; fps: number }> = ({ beat, frame, fps }) => {
  const p = progress(frame, fps, beat.startSec, 0.5);
  return (
    <div style={{ transform: `translateY(${(1 - p) * 28}px)`, opacity: p }}>
      <div style={{ color: blue, fontSize: 28, fontWeight: 950 }}>{beat.layout.replace("-", " / ")}</div>
      <div style={{ marginTop: 18, color: ink, fontSize: 78, lineHeight: 1.03, fontWeight: 950, letterSpacing: 0 }}>
        {beat.title}
      </div>
      {beat.subtitle && (
        <div
          style={{
            marginTop: 22,
            display: "inline-block",
            padding: "14px 20px",
            borderRadius: 999,
            background: "#fff2b8",
            color: "#713f12",
            fontSize: 32,
            fontWeight: 900,
          }}
        >
          {beat.subtitle}
        </div>
      )}
    </div>
  );
};

const CompareScene: FC<{ beat: VisualBeat; frame: number; fps: number }> = ({ beat, frame, fps }) => (
  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 22, marginTop: 42 }}>
    {(beat.bullets ?? ["wrong", "right"]).slice(0, 2).map((item, index) => {
      const p = progress(frame, fps, beat.startSec + 0.18 + index * 0.2, 0.45);
      return (
        <div
          key={item}
          style={{
            ...card,
            minHeight: 380,
            padding: 30,
            borderColor: index === 0 ? "rgba(239,68,68,0.28)" : "rgba(34,197,94,0.28)",
            background: index === 0 ? "rgba(254,242,242,0.95)" : "rgba(240,253,244,0.95)",
            transform: `translateY(${(1 - p) * 60}px) scale(${0.96 + p * 0.04})`,
            opacity: p,
          }}
        >
          <div style={{ fontSize: 26, color: index === 0 ? "#dc2626" : "#16a34a", fontWeight: 950 }}>
            {index === 0 ? "错误方式" : "正确方式"}
          </div>
          <div style={{ marginTop: 56, fontSize: 46, lineHeight: 1.12, fontWeight: 950 }}>{item}</div>
        </div>
      );
    })}
  </div>
);

const MainScene: FC<{ beat: VisualBeat; frame: number; fps: number }> = ({ beat, frame, fps }) => {
  if (beat.layout === "wrong-right" || beat.layout === "compare") {
    return <CompareScene beat={beat} frame={frame} fps={fps} />;
  }
  return <AssetPanel beat={beat} frame={frame} fps={fps} />;
};

export const VideoGrowthTemplate: FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;
  const beats = episodeManifest.visualPlan.beats;
  const beat = activeBeat(sec, beats);
  const caption = activeCaption(sec, episodeManifest.captions.data);

  return (
    <Shell>
      <BrandBar />
      <div style={{ position: "absolute", inset: "116px 58px 178px", zIndex: 10, ...sceneStyle(frame, fps, beat) }}>
        <TitleBlock beat={beat} frame={frame} fps={fps} />
        <MainScene beat={beat} frame={frame} fps={fps} />
      </div>
      <CaptionLine caption={caption} terms={episodeManifest.captions.highlightTerms} />
      <div style={{ position: "absolute", left: 58, right: 58, bottom: 54, height: 9, borderRadius: 999, background: "rgba(15,23,42,0.1)" }}>
        <div
          style={{
            width: `${Math.min(100, (sec / episodeManifest.video.durationSec) * 100)}%`,
            height: "100%",
            borderRadius: 999,
            background: `linear-gradient(90deg, ${blue}, ${cyan}, ${yellow})`,
          }}
        />
      </div>
      {episodeManifest.voice?.path ? <Audio src={staticFile(episodeManifest.voice.path)} /> : null}
      {episodeManifest.bgm?.path ? <Audio src={staticFile(episodeManifest.bgm.path)} volume={episodeManifest.bgm.volume ?? 0.18} /> : null}
    </Shell>
  );
};
