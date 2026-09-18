
"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

interface CivicResponse {
  intent: string;
  language: string;
  title: string;
  summary: string;
  eligibility?: string;
  steps: string[];
  documents: string[];
  department?: string;
  application_channel?: string;
  source_title?: string;
  source_url?: string;
  last_verified?: string;
}

interface SimplifyResponse {
  explanation: string;
  model: string;
}

interface DocumentAnalysisResponse {
  document_type: string;
  title: string;
  summary: string;
  important_information: string[];
  eligibility: string[];
  deadlines: string[];
  required_documents: string[];
  steps: string[];
  warnings: string[];
}

export default function Home() {
  // --------------------------------
  // General state
  // --------------------------------
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState("en");

  // --------------------------------
  // CivicBridge response
  // --------------------------------
  const [response, setResponse] = useState<CivicResponse | null>(null);
  const [loading, setLoading] = useState(false);

  // --------------------------------
  // Optional AI simplification
  // --------------------------------
  const [simplifying, setSimplifying] = useState(false);
  const [simplifiedResponse, setSimplifiedResponse] =
  useState<SimplifyResponse | null>(null);
  const [simplifyError, setSimplifyError] = useState("");
  


  const [selectedModel, setSelectedModel] = useState(
    "gemini-3.5-flash-lite"
  );

  // --------------------------------
  // Government PDF analysis
  // --------------------------------
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [documentAnalysis, setDocumentAnalysis] =
    useState<DocumentAnalysisResponse | null>(null);
  const [documentLoading, setDocumentLoading] = useState(false);
  const [documentError, setDocumentError] = useState("");

  // --------------------------------
  // Backend URL
  // --------------------------------
  const API_URL = "http://localhost:8000";

  // --------------------------------
  // Deterministic CivicBridge answer
  // --------------------------------
  async function askCivicBridge() {
    if (!message.trim()) return;

    setLoading(true);
    setResponse(null);
    setSimplifiedResponse(null);

    try {
      const result = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
          language,
        }),
      });

      const data = await result.json();

      if (!result.ok) {
        throw new Error(
          data.detail || "CivicBridge request failed."
        );
      }

      setResponse(data);
    } catch (error) {
      console.error(error);

      alert(
        error instanceof Error
          ? error.message
          : "CivicBridge is temporarily unavailable."
      );
    } finally {
      setLoading(false);
    }
  }

  // --------------------------------
  // Optional AI simplification
  // --------------------------------
  async function simplifyAnswer() {
    if (!response) return;

    setSimplifying(true);
    setSimplifiedResponse(null);
    setSimplifyError("");

    try {
      const result = await fetch(
        `${API_URL}/api/chat/simplify`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message,
            language: response.language || "en",
            model: selectedModel,
          }),
        }
      );

      const data = await result.json();

      if (!result.ok) {
        throw new Error(
          data.detail || "AI simplification failed."
        );
      }

      setSimplifiedResponse(data);
    } catch (error) {
      console.error(error);

      setSimplifyError(
        error instanceof Error
          ? error.message
          : "AI simplification is temporarily unavailable. Please try again."
      );
    } finally {
      setSimplifying(false);
    }
  }

  // --------------------------------
  // Government PDF document analysis
  // --------------------------------
  async function analyzeDocument() {
    if (!selectedFile) return;

    setDocumentLoading(true);
    setDocumentError("");
    setDocumentAnalysis(null);

    // Basic frontend validation
    if (selectedFile.type !== "application/pdf") {
      setDocumentError("Please select a PDF file.");
      setDocumentLoading(false);
      return;
    }

    // 20 MB frontend limit
    const MAX_FILE_SIZE = 20 * 1024 * 1024;

    if (selectedFile.size > MAX_FILE_SIZE) {
      setDocumentError(
        "The PDF is too large. Please select a file smaller than 20 MB."
      );
      setDocumentLoading(false);
      return;
    }

    const formData = new FormData();

    formData.append("file", selectedFile);
    formData.append("model", selectedModel);
    formData.append("language", language);

    try {
      const result = await fetch(
        `${API_URL}/api/analyze-document`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await result.json();

      if (!result.ok) {
        throw new Error(
          data.detail || "Document analysis failed."
        );
      }

      setDocumentAnalysis(data);
    } catch (error) {
      console.error(error);

      setDocumentError(
        error instanceof Error
          ? error.message
          : "Document analysis failed."
      );
    } finally {
      setDocumentLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-16">
      <div className="mx-auto max-w-3xl">

        {/* ========================================= */}
        {/* Header */}
        {/* ========================================= */}

        <div className="text-center">
          <h1 className="text-5xl font-bold tracking-tight">
            CivicBridge
          </h1>

          <p className="mt-4 text-xl text-slate-600">
            Government, made understandable.
          </p>
        </div>

        {/* ========================================= */}
        {/* Civic Question */}
        {/* ========================================= */}

        <div className="mt-12 rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">
            Ask CivicBridge
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            Ask a question about a government service, scheme, or
            civic process.
          </p>

          {/* Language */}
          <div className="mt-6">
            <label className="text-sm font-medium text-slate-700">
              Language
            </label>

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-300 bg-white p-3 outline-none focus:border-slate-500"
            >
              <option value="en">English</option>
              <option value="te">తెలుగు</option>
            </select>
          </div>

          {/* Question */}
          <label className="mt-6 block text-sm font-medium text-slate-700">
            What do you need help with?
          </label>

          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="For example: My land records have the wrong name..."
            className="mt-3 min-h-32 w-full rounded-xl border border-slate-300 p-4 outline-none focus:border-slate-500"
          />

          {/* Ask button */}
          <button
            onClick={askCivicBridge}
            disabled={!message.trim() || loading}
            className="mt-4 rounded-xl bg-slate-900 px-6 py-3 font-medium text-white disabled:opacity-50"
          >
            {loading ? "Understanding..." : "Ask CivicBridge"}
          </button>
        </div>

        {/* ========================================= */}
        {/* Government PDF Analysis */}
        {/* ========================================= */}

        <div className="mt-8 rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">
            Analyze a Government PDF
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            Upload a government notice, order, or civic document
            and CivicBridge will explain what it contains.
          </p>

          {/* File selection */}
          <div className="mt-5">
            <label className="text-sm font-medium text-slate-700">
              Select PDF
            </label>

            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => {
                const file = e.target.files?.[0] ?? null;

                setSelectedFile(file);
                setDocumentAnalysis(null);
                setDocumentError("");

                if (!file) return;

                if (file.type !== "application/pdf") {
                  setDocumentError(
                    "Please select a PDF file."
                  );
                  return;
                }

                const MAX_FILE_SIZE = 20 * 1024 * 1024;

                if (file.size > MAX_FILE_SIZE) {
                  setDocumentError(
                    "The PDF is too large. Please select a file smaller than 20 MB."
                  );
                }
              }}
              className="mt-2 block w-full rounded-xl border border-slate-300 bg-white p-3 text-sm"
            />

            {selectedFile && (
              <p className="mt-3 text-sm text-slate-600">
                Selected: {selectedFile.name}
              </p>
            )}
          </div>

          {/* Model selection */}
          <div className="mt-5">
            <label className="text-sm font-medium text-slate-700">
              AI model
            </label>

            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-300 bg-white p-3 outline-none focus:border-slate-500"
            >
              <option value="gemini-3.6-flash">
                Gemini 3.6 Flash
              </option>

              <option value="gemini-3.5-flash-lite">
                Gemini 3.5 Flash-Lite
              </option>
            </select>
          </div>

          {/* Document error */}
          {documentError && (
            <div className="mt-4 rounded-xl bg-red-50 p-4 text-sm text-red-700">
              <p>{documentError}</p>

              <p className="mt-1 text-xs text-red-600">
                You can try analyzing the same PDF again.
              </p>
            </div>
          )}

          {/* Analyze button */}
          <button
            onClick={analyzeDocument}
            disabled={
              !selectedFile ||
              documentLoading
            }
            className="mt-4 rounded-xl bg-slate-900 px-6 py-3 font-medium text-white disabled:opacity-50"
          >
            {documentLoading
              ? "Analyzing document..."
              : documentError
              ? "Try Again"
              : "Analyze PDF"}
          </button>
        </div>

        {/* ========================================= */}
        {/* Document Analysis Result */}
        {/* ========================================= */}

        {documentAnalysis && (
          <div className="mt-8 rounded-2xl bg-white p-6 shadow-sm">

            {/* Document type */}
            <p className="text-sm font-medium text-slate-500">
              Document Type
            </p>

            <p className="mt-1 font-medium text-slate-700">
              {documentAnalysis.document_type}
            </p>

            {/* Title */}
            <h2 className="mt-4 text-2xl font-bold">
              {documentAnalysis.title}
            </h2>

            {/* Summary */}
            <p className="mt-4 text-slate-700">
              {documentAnalysis.summary}
            </p>

            {/* Important Information */}
            {documentAnalysis.important_information.length > 0 && (
              <div className="mt-8">
                <h3 className="font-semibold">
                  Important information
                </h3>

                <ul className="mt-3 space-y-2">
                  {documentAnalysis.important_information.map(
                    (item, index) => (
                      <li
                        key={index}
                        className="rounded-xl bg-slate-50 p-3 text-slate-700"
                      >
                        {item}
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

            {/* Eligibility */}
            {documentAnalysis.eligibility.length > 0 && (
              <div className="mt-8">
                <h3 className="font-semibold">
                  Eligibility
                </h3>

                <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
                  {documentAnalysis.eligibility.map(
                    (item, index) => (
                      <li key={index}>{item}</li>
                    )
                  )}
                </ul>
              </div>
            )}

            {/* Deadlines */}
            {documentAnalysis.deadlines.length > 0 && (
              <div className="mt-8 rounded-xl bg-slate-50 p-4">
                <h3 className="font-semibold">
                  Deadlines
                </h3>

                <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
                  {documentAnalysis.deadlines.map(
                    (item, index) => (
                      <li key={index}>{item}</li>
                    )
                  )}
                </ul>
              </div>
            )}

            {/* Required Documents */}
            {documentAnalysis.required_documents.length > 0 && (
              <div className="mt-8">
                <h3 className="font-semibold">
                  Required documents
                </h3>

                <ul className="mt-3 space-y-2">
                  {documentAnalysis.required_documents.map(
                    (item, index) => (
                      <li
                        key={index}
                        className="flex items-start gap-3 rounded-xl bg-slate-50 p-3 text-slate-700"
                      >
                        <span>✓</span>
                        <span>{item}</span>
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

            {/* Steps */}
            {documentAnalysis.steps.length > 0 && (
              <div className="mt-8">
                <h3 className="font-semibold">
                  What the document says to do
                </h3>

                <ol className="mt-3 list-decimal space-y-2 pl-5 text-slate-700">
                  {documentAnalysis.steps.map(
                    (step, index) => (
                      <li key={index}>{step}</li>
                    )
                  )}
                </ol>
              </div>
            )}

            {/* Warnings */}
            {documentAnalysis.warnings.length > 0 && (
              <div className="mt-8 rounded-xl bg-amber-50 p-4">
                <h3 className="font-semibold text-amber-900">
                  Important warnings
                </h3>

                <ul className="mt-3 list-disc space-y-2 pl-5 text-amber-800">
                  {documentAnalysis.warnings.map(
                    (warning, index) => (
                      <li key={index}>{warning}</li>
                    )
                  )}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* ========================================= */}
        {/* Deterministic CivicBridge Response */}
        {/* ========================================= */}

        {response && (
          <div className="mt-8 rounded-2xl bg-white p-6 shadow-sm">

            <p className="text-sm font-medium text-slate-500">
              We understood this as
            </p>

            <h2 className="mt-1 text-2xl font-bold">
              {response.title}
            </h2>

            <p className="mt-4 text-slate-700">
              {response.summary}
            </p>

            {/* Eligibility */}
            {response.eligibility && (
              <div className="mt-6 rounded-xl bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-500">
                  Who this is for
                </p>

                <p className="mt-1 text-slate-700">
                  {response.eligibility}
                </p>
              </div>
            )}

            {/* Steps */}
            <h3 className="mt-8 font-semibold">
              What happens next?
            </h3>

            <ol className="mt-3 list-decimal space-y-2 pl-5 text-slate-700">
              {response.steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>

            {/* Documents */}
            {response.documents.length > 0 && (
              <div className="mt-8">
                <h3 className="font-semibold">
                  Documents you may need
                </h3>

                <ul className="mt-3 space-y-2">
                  {response.documents.map(
                    (document, index) => (
                      <li
                        key={index}
                        className="flex items-start gap-3 rounded-xl bg-slate-50 p-3 text-slate-700"
                      >
                        <span className="mt-0.5">✓</span>
                        <span>{document}</span>
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

            {/* Department */}
            {response.department && (
              <div className="mt-8 rounded-xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">
                  Relevant department
                </p>

                <p className="mt-1 font-medium">
                  {response.department}
                </p>
              </div>
            )}

            {/* Application Channel */}
            {response.application_channel && (
              <div className="mt-4 rounded-xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">
                  Where to apply
                </p>

                <p className="mt-1 font-medium">
                  {response.application_channel}
                </p>
              </div>
            )}

            {/* Official Source */}
            {response.source_title && (
              <div className="mt-8 border-t border-slate-200 pt-5">
                <p className="text-sm text-slate-500">
                  Official source
                </p>

                {response.source_url ? (
                  <a
                    href={response.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-1 inline-block font-medium text-blue-700 underline"
                  >
                    {response.source_title}
                  </a>
                ) : (
                  <p className="mt-1 font-medium">
                    {response.source_title}
                  </p>
                )}

                {response.last_verified && (
                  <p className="mt-2 text-xs text-slate-500">
                    Verified: {response.last_verified}
                  </p>
                )}
              </div>
            )}

            {/* ========================================= */}
            {/* Optional AI Simplification */}
            {/* ========================================= */}

            <div className="mt-10 border-t border-slate-200 pt-6">

              <p className="font-semibold">
                Want this explained more simply?
              </p>

              <p className="mt-1 text-sm text-slate-500">
                CivicBridge can optionally use AI to make the
                answer easier to understand.
              </p>

              {/* Model selector */}
              <div className="mt-4">
                <label className="text-sm font-medium text-slate-700">
                  Choose AI model
                </label>

                <select
                  value={selectedModel}
                  onChange={(e) =>
                    setSelectedModel(e.target.value)
                  }
                  className="mt-2 w-full rounded-xl border border-slate-300 bg-white p-3 outline-none focus:border-slate-500"
                >
                  <option value="gemini-3.6-flash">
                    Gemini 3.6 Flash
                  </option>

                  <option value="gemini-3.5-flash-lite">
                    Gemini 3.5 Flash-Lite
                  </option>
                </select>
              </div>

              {/* Simplify button */}
              <button
                onClick={simplifyAnswer}
                disabled={!response || simplifying}
                className="mt-4 rounded-xl bg-blue-600 px-5 py-3 font-medium text-white disabled:opacity-50"
              >
                {simplifying
                  ? "Simplifying..."
                  : "✨ Simplify with AI"}
              </button>


              {/* AI simplification error */}
              {simplifyError && (
                <div className="mt-6 rounded-xl bg-red-50 p-4 text-sm text-red-700">
                  <p>{simplifyError}</p>
                  <button
                  onClick={simplifyAnswer}
                  disabled={simplifying}
                  className="mt-3 rounded-lg bg-red-700 px-4 py-2 font-medium text-white disabled:opacity-50"
                  >
                    {simplifying ? "Trying again..." : "Try Again"}
                  </button>
                  </div>
              )}


              {/* AI response */}
              {simplifiedResponse && (
                <div className="mt-6 rounded-xl bg-blue-50 p-5">

                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-blue-900">
                      ✨ AI explanation
                    </p>

                    <span className="text-xs text-blue-700">
                      {simplifiedResponse.model}
                    </span>
                  </div>

                  {/* <p className="mt-3 whitespace-pre-line text-slate-700">
                    {simplifiedResponse.explanation}
                  </p> */}
                  <div className="mt-3 prose prose-sm max-w-none text-slate-700">
                    <ReactMarkdown>
                      {simplifiedResponse.explanation}
                    </ReactMarkdown>
                    </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

