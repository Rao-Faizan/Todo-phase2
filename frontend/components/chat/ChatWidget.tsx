'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useSearchParams } from 'next/navigation';
import { Send, Bot, User } from 'lucide-react';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export default function ChatWidget() {
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', content: 'Hello! How can I help you with your tasks today?', role: 'assistant', timestamp: new Date() }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const messageText = inputValue.trim();
    if (!messageText || isLoading || !isAuthenticated) {
      console.log('Chat submit blocked:', { messageText, isLoading, isAuthenticated });
      return;
    }

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      content: messageText,
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const { sendChatMessage } = await import('@/lib/api-client');
      const data = await sendChatMessage(messageText);

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response || 'I processed your request.',
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error: any) {
      console.error('Chat Error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: error.message || 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[500px] bg-slate-800/50">
      <div className="p-4 border-b border-white/10 flex items-center gap-2">
        <Bot className="w-5 h-5 text-primary-400" />
        <h2 className="text-lg font-semibold text-white">AI Assistant</h2>
      </div>

      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex gap-3 max-w-[80%]`}>
              {message.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-primary-600/20 flex items-center justify-center flex-shrink-0 border border-primary-500/20">
                  <Bot className="w-4 h-4 text-primary-400" />
                </div>
              )}
              <div
                className={`px-4 py-2 rounded-2xl ${message.role === 'user'
                  ? 'bg-primary-600 text-white rounded-tr-sm'
                  : 'bg-slate-700 text-gray-200 rounded-tl-sm border border-white/5'
                  }`}
              >
                {message.content}
              </div>
              {message.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0 border border-white/10">
                  <User className="w-4 h-4 text-gray-400" />
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="w-8 h-8 rounded-full bg-primary-600/20 flex items-center justify-center flex-shrink-0 mr-3">
              <Bot className="w-4 h-4 text-primary-400" />
            </div>
            <div className="bg-slate-700 text-gray-400 px-4 py-2 rounded-2xl rounded-tl-sm border border-white/5 animate-pulse">
              Thinking...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-white/10 flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask AI helper..."
          className="flex-grow bg-slate-900/50 border border-white/10 rounded-xl px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 placeholder:text-gray-600"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="bg-primary-600 text-white p-2 rounded-xl hover:bg-primary-500 disabled:opacity-50 transition-colors"
          disabled={isLoading || !inputValue.trim()}
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
}