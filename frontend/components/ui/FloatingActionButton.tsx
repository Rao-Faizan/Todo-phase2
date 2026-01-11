import { PlusIcon } from '@heroicons/react/24/outline';

interface FloatingActionButtonProps {
  onClick: () => void;
  ariaLabel?: string;
}

export function FloatingActionButton({ onClick, ariaLabel = 'Add new task' }: FloatingActionButtonProps) {
  return (
    <button
      onClick={onClick}
      aria-label={ariaLabel}
      className="fixed bottom-6 right-6 bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-700 hover:to-indigo-700 text-white p-4 rounded-full shadow-lg shadow-primary-500/30 hover:shadow-xl hover:shadow-primary-500/50 transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900"
    >
      <PlusIcon className="h-6 w-6" />
    </button>
  );
}