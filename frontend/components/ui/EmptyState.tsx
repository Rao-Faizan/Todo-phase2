import { PlusIcon } from '@heroicons/react/24/outline';

interface EmptyStateProps {
  title?: string;
  description?: string;
  showButton?: boolean;
  onActionClick?: () => void;
  actionText?: string;
}

export function EmptyState({
  title = 'No tasks yet',
  description = 'Get started by creating your first task',
  showButton = false,
  onActionClick,
  actionText = 'Create Task'
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900/30 dark:to-primary-800/20 w-24 h-24 rounded-full flex items-center justify-center mb-6">
        <div className="bg-primary-200 dark:bg-primary-800/50 w-16 h-16 rounded-full flex items-center justify-center">
          <span className="text-3xl">📝</span>
        </div>
      </div>
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-md">{description}</p>
      {showButton && (
        <button
          onClick={onActionClick}
          className="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-all duration-300 shadow-sm hover:shadow-md"
        >
          <PlusIcon className="h-5 w-5" />
          {actionText}
        </button>
      )}
    </div>
  );
}