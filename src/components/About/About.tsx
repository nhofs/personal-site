export function About() {
  return (
    <section id="about" className="section-container bg-gray-900/50">
      <div className="max-w-4xl mx-auto text-center">
        <div className="grid md:grid-cols-2 gap-8 text-left">
          <div className="flex items-center">
            <div className="space-y-6">
              <img
                src="./profile.jpg"
                alt="Nolan Hofstee"
                className="w-48 h-48 rounded-2xl object-cover border-2 border-green-500/30 mx-auto"
              />
              <div className="space-y-4">
                <p className="text-gray-300 leading-relaxed">
                  Software engineer who found his calling in code after a year of med school.
                  Started as a support agent at DoorLoop, earned a promotion to QA Engineer
                  within a year, and now building software full-time while waiting on my
                  next promotion to Software Engineer.
                </p>
                <p className="text-gray-300 leading-relaxed">
                  Outside of work, I'm self-hosting side apps for my family, experimenting
                  with AI models on a Linux server, and building small games in Godot.
                  When I'm not at a keyboard, you'll find me rock climbing, hiking 20-mile
                  trails, or gaming. I'm a firm believer in clever solutions over bought ones.
                </p>
              </div>
            </div>
          </div>
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold text-white text-center pb-2">Technologies</h3>
            <div className="grid grid-cols-2 gap-4">
              {[
                "React",
                "TypeScript",
                "React Native",
                "Expo",
                "Node.js",
                "MongoDB",
                "Godot",
                "Cloudflare",
                "Docker",
              ].map((tech) => (
                <span
                  key={tech}
                  style={{ padding: "20px 24px" }}
                  className="text-center bg-green-500/10 border-2 border-green-500/30 rounded-full text-sm text-green-400 font-medium"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
