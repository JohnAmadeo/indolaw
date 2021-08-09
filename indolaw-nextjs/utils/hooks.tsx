import { useState, useEffect } from 'react';

export function useIsMobile() {
  const [isMobileDevice, setIsMobileDevice] = useState(false);

  useEffect(() => {
    async function detectDevice() {
      const { isMobile } = await import('react-device-detect');
      setIsMobileDevice(isMobile);
    }

    detectDevice();
  }, [setIsMobileDevice]);

  return isMobileDevice;
}