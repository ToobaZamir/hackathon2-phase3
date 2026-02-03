interface SkeletonLoaderProps {
  count?: number;
  height?: string;
  width?: string;
  className?: string;
}

const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  count = 1,
  height = 'h-4',
  width = 'w-full',
  className = ''
}) => {
  const skeletons = Array.from({ length: count }, (_, index) => (
    <div
      key={index}
      className={`${height} ${width} bg-gray-200 rounded animate-pulse ${className}`}
    />
  ));

  return <>{skeletons}</>;
};

export default SkeletonLoader;