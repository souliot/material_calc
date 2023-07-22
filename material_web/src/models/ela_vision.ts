import { useState } from 'react';

export default function ElaVision() {
  const [downloadLoading, setDownloadLoading] = useState<boolean>(false);
  const [curDir, setCurDir] = useState<any>();
  const [calcRes, setCalcRes] = useState<any>();

  return {
    downloadLoading,
    setDownloadLoading,
    calcRes,
    setCalcRes,
    curDir,
    setCurDir,
  };
}
