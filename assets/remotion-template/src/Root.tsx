import { Composition } from "remotion";
import { VideoGrowthTemplate } from "./VideoGrowthTemplate";

export const Root: React.FC = () => (
  <Composition
    id="VideoGrowthTemplate"
    component={VideoGrowthTemplate}
    durationInFrames={45 * 30}
    fps={30}
    width={1080}
    height={1920}
  />
);

