import React, { useRef, useState, useEffect } from "react";
import axios from "axios";
import { Send, Upload, AlertCircle, Book, MessageSquare, FileText } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import toast, { Toaster } from "react-hot-toast";

interface Citation {
  page: string;
  content: string;
  title?: string;
  author?: string;
}

interface QAResponse {
  answer: string;
  citations: Citation[];
  follow_up_questions: string[];
  disclaimer: string;
  confidence_level: string;
}

const App = () => {
  const [response, setResponse] = useState<QAResponse | null>(null);
  const [history, setHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  const fetchChatHistory = async () => {
    try {
      const response = await axios.get("http://localhost:8000/chat_history/");
      const chatHistory = response.data.chat_history
        .filter((item: any, index: number) => typeof item === "object" && item.content && index % 2 == 0)
        .map((item: any) => item.content);
      setHistory(chatHistory);
    } catch (error) {
      console.error("Error fetching chat history:", error);
    }
  };

  const handleSend = async () => {
    const query = inputRef.current?.value;
    if (!query?.trim()) {
      toast.error("Please enter your medical question.");
      return;
    }

    setLoading(true);
    const toastId = toast.loading("Processing your question...");

    try {
      // Modified request to send query parameter
      const resp = await axios.post<QAResponse>(
        `http://localhost:8000/ask_question?question=${encodeURIComponent(query)}`,
        {
          headers: { "Content-Type": "application/json" }, 
        }
      );

      setResponse(resp.data);
      fetchChatHistory();
      if (inputRef.current) inputRef.current.value = "";
      toast.success("Response received!", { id: toastId });
    } catch (error: any) {
      console.error(error);
      toast.error(error.response?.data?.detail || "Failed to process question", { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 overflow-hidden">
      <Toaster position="top-right" />
      
      {/* Rest of the component remains the same */}
      <aside className="w-64 bg-gray-800 shadow-lg">
        <div className="p-4 border-b border-gray-700">
          <h1 className="text-xl font-bold text-gray-100 flex items-center gap-2">
            <Book className="w-5 h-5" />
            Medical Assistant
          </h1>
        </div>
        
        <div className="p-4">
          <h2 className="text-sm font-semibold text-gray-300 flex items-center gap-2 mb-4">
            <MessageSquare className="w-4 h-4" />
            Chat History
          </h2>
          <div className="h-screen space-y-2 overflow-y-auto">
            {history.map((message, index) => (
              <div key={index} className="p-2 text-sm bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600">
                {message}
              </div>
            ))}
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col">
        <div className="p-4 bg-gray-800 shadow">
          <Alert variant="default" className="bg-yellow-900 border-yellow-700">
            <AlertCircle className="h-4 w-4 text-yellow-400" />
            <AlertDescription className="text-yellow-100">
              This system provides general medical information for educational purposes only.
              Always consult healthcare professionals for medical advice.
            </AlertDescription>
          </Alert>
        </div>

        <div className="flex-1 overflow-auto p-6 bg-gray-900">
          {response && (
            <div className="space-y-6">
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                <h3 className="text-lg font-semibold mb-2 text-gray-100">Response</h3>
                <p className="text-gray-300">{response.answer}</p>
                
                <div className="mt-4 flex items-center">
                  <span className="text-sm font-medium text-gray-400">Confidence Level:</span>
                  <span className={`ml-2 px-2 py-1 text-sm rounded ${
                    response.confidence_level.startsWith("High") ? "bg-green-900 text-green-200" :
                    response.confidence_level.startsWith("Medium") ? "bg-yellow-900 text-yellow-200" :
                    "bg-red-900 text-red-200"
                  }`}>
                    {response.confidence_level}
                  </span>
                </div>
              </div>

              {response.citations.length > 0 && (
                <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-gray-100">
                    <FileText className="w-5 h-5" />
                    Source Citations
                  </h3>
                  <div className="space-y-4">
                    {response.citations.map((citation, index) => (
                      <div key={index} className="p-4 bg-gray-700 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                          {citation.title && (
                            <span className="text-sm font-medium text-gray-200">
                              {citation.title}
                            </span>
                          )}
                          {citation.page && (
                            <span className="text-sm text-gray-400">
                              Page {citation.page}
                            </span>
                          )}
                        </div>
                        <p className="text-gray-300 text-sm">{citation.content}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {response.follow_up_questions.length > 0 && (
                <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                  <h3 className="text-lg font-semibold mb-4 text-gray-100">Suggested Follow-up Questions</h3>
                  <div className="space-y-2">
                    {response.follow_up_questions.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => {
                          if (inputRef.current) inputRef.current.value = question;
                        }}
                        className="block w-full text-left p-3 text-sm bg-blue-900 hover:bg-blue-800 rounded-lg text-blue-100 transition-colors"
                      >
                        {question}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="p-4 bg-gray-800 border-t border-gray-700">
          <div className="max-w-4xl mx-auto space-y-4">
            <div className="flex items-center gap-2">
              <input
                ref={inputRef}
                type="text"
                placeholder="Ask your medical question..."
                className="flex-1 px-4 py-2 bg-gray-700 text-gray-100 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              />
              <button
                onClick={handleSend}
                disabled={loading}
                className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;