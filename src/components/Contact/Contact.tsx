import { useState } from "react";

export function Contact() {
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "error">("idle");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("sending");
    const form = e.currentTarget;
    const data = new FormData(form);

    try {
      const res = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: data,
      });
      if (res.ok) {
        setStatus("sent");
        form.reset();
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  }

  return (
    <section id="contact" className="section-container bg-gray-900/50">
      <div className="max-w-2xl mx-auto w-full">
        <h2 className="text-3xl md:text-4xl font-bold mb-8 text-center text-white">
          Get in Touch
        </h2>
        <p className="text-center text-gray-400 mb-8">
          I'm always open to discussing new projects, creative ideas, or opportunities
          to be part of your vision.
        </p>
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="hidden"
            name="access_key"
            value={import.meta.env.VITE_WEB3_ACCESS_KEY ?? ""}
          />
          <div>
            <label htmlFor="name" className="block text-sm text-gray-400 mb-2">
              Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-green-500 focus:outline-none transition-colors"
              placeholder="Your name"
            />
          </div>
          <div>
            <label htmlFor="email" className="block text-sm text-gray-400 mb-2">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-green-500 focus:outline-none transition-colors"
              placeholder="your@email.com"
            />
          </div>
          <div>
            <label htmlFor="message" className="block text-sm text-gray-400 mb-2">
              Message
            </label>
            <textarea
              id="message"
              name="message"
              rows={5}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-green-500 focus:outline-none transition-colors resize-none"
              placeholder="Your message..."
            />
          </div>
          <button
            type="submit"
            disabled={status === "sending"}
            className="w-full py-3 bg-green-500/20 border border-green-500/50 rounded-lg text-green-400 hover:bg-green-500/30 transition-colors disabled:opacity-50"
          >
            {status === "sending" ? "Sending..." : status === "sent" ? "Sent!" : "Send Message"}
          </button>
          {status === "error" && (
            <p className="text-red-400 text-sm text-center">Something went wrong. Try again later.</p>
          )}
        </form>
        <div className="mt-12 flex justify-center gap-6">
          <a
            href="https://github.com/nhofs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-white transition-colors"
          >
            GitHub
          </a>
          <a
            href="https://www.linkedin.com/in/nolan-hofstee-15303723a/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-white transition-colors"
          >
            LinkedIn
          </a>
          <a
            href="https://discord.com/users/fapplejack13"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-white transition-colors"
          >
            Discord
          </a>
        </div>
      </div>
    </section>
  );
}
