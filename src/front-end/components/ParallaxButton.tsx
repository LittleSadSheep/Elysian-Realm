import React, { useRef } from 'react';
import './ParallaxButton.css';

interface ParallaxButtonProps {
  icon: React.ReactNode;
  label: string;
  selected?: boolean;
  onClick?: () => void;
  flyToTop?: boolean;
  flatGlass?: boolean; // 新增属性
  style?: React.CSSProperties;
}

const ParallaxButton: React.FC<ParallaxButtonProps> = ({ icon, label, selected, onClick, flyToTop, flatGlass, style }) => {
  const btnRef = useRef<HTMLButtonElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    const btn = btnRef.current;
    if (!btn) return;
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `perspective(600px) scale(1.06) rotateY(${-x / 18}deg) rotateX(${y / 18}deg)`;
  };
  const handleMouseLeave = () => {
    const btn = btnRef.current;
    if (!btn) return;
    btn.style.transform = '';
  };

  return (
    <button
      ref={btnRef}
      className={
        flatGlass
          ? `flat-glass-btn${selected ? ' selected' : ''}`
          : `parallax-btn fluid-btn${selected ? ' selected' : ''}${flyToTop ? ' fly-top' : ''}`
      }
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      style={style}
    >
      <span className="parallax-btn-icon">{icon}</span>
      <span className="parallax-btn-label">{label}</span>
    </button>
  );
};

export default ParallaxButton;
