export function TaskSkeleton() {
  return (
    <div className="bg-white dark:bg-dark-800/80 backdrop-blur-sm border border-gray-200 dark:border-dark-700 rounded-2xl p-6 shadow-lg animate-pulse">
      <div className="flex items-start gap-4">
        <div className="w-6 h-6 rounded-full bg-gray-200 dark:bg-dark-700 mt-1"></div>
        <div className="flex-1 space-y-3">
          <div className="h-5 bg-gray-200 dark:bg-dark-700 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 dark:bg-dark-700 rounded w-full"></div>
          <div className="h-4 bg-gray-200 dark:bg-dark-700 rounded w-2/3"></div>
          <div className="h-8 w-24 bg-gray-200 dark:bg-dark-700 rounded mt-4"></div>
        </div>
      </div>
    </div>
  );
}