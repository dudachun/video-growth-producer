export type Caption = {
  text: string;
  startMs: number;
  endMs: number;
};

export type VisualBeat = {
  startSec: number;
  endSec: number;
  layout:
    | "impact-open"
    | "wrong-right"
    | "compare"
    | "workflow"
    | "proof"
    | "screen-demo"
    | "checklist"
    | "asset-focus"
    | "cta";
  title: string;
  subtitle?: string;
  visualGoal: string;
  assetSource: "imagegen" | "official" | "screenshot" | "generated-ui" | "none";
  asset?: string;
  imagegenAsset?: string;
  bullets?: string[];
  motion: string[];
};

export type EpisodeManifest = {
  mode: "strict" | "remotion-only";
  episodeId: string;
  title: string;
  seriesName?: string;
  video: {
    width: number;
    height: number;
    fps: number;
    durationSec: number;
    captionTopPercent: number;
    captionFont?: string;
    captionHighlightColor?: string;
  };
  voice?: {
    path?: string;
    speed?: number;
    openingQaPassed?: boolean;
  };
  bgm?: {
    path?: string;
    volume?: number;
  };
  captions: {
    highlightTerms: string[];
    data: Caption[];
  };
  visualPlan: {
    beats: VisualBeat[];
  };
};
