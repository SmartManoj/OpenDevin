import React from "react";
import JupyterEditor from "#/components/Jupyter";

function Jupyter() {
  const parentRef = React.useRef<HTMLDivElement>(null);
  const [parentWidth, setParentWidth] = React.useState(0);

  // This is a hack to prevent the editor from overflowing
  // Should be removed after revising the parent and containers
  React.useEffect(() => {
    if (parentRef.current) {
      setParentWidth(parentRef.current.offsetWidth);
    }
  }, []);

  return (
    <div ref={parentRef} style={{ height: "100%" }}>
      <JupyterEditor maxWidth={parentWidth} />
    </div>
  );
}

export default Jupyter;
