import type { FC } from "react";
import { Composition } from "remotion";
import { episodeManifest } from "./episode_manifest";
import { VideoGrowthTemplate } from "./VideoGrowthTemplate";

export const Root: FC = () => (
  <Composition
    id="VideoGrowthTemplate"
    component={VideoGrowthTemplate}
    durationInFrames={Math.ceil(episodeManifest.video.durationSec * episodeManifest.video.fps)}
    fps={episodeManifest.video.fps}
    width={episodeManifest.video.width}
    height={episodeManifest.video.height}
  />
);
