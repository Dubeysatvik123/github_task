import google.generativeai as genai
import gradio as gr
import time

genai.configure(api_key="AIzaSyAAdwMJ2cO-Cqp76d8J_beTwYNE2EahyXI")
model = genai.GenerativeModel("gemini-1.5-flash")

def evaluate_startup_idea(prompt, progress=gr.Progress()):
    """Evaluate startup idea with progress tracking"""
    if not prompt.strip():
        return "Please enter your startup idea to get an evaluation."
    
    # Progress tracking
    progress(0.1, desc="Initializing evaluation...")
    
    system_prompt = """You are a seasoned project architect and startup strategist. For the idea I provide, give a brief, structured evaluation across these 5 pillars:

1. **Feasibility** 🔧
   - Is it technically doable today?
   - Do similar products exist? If yes, what's the clear differentiator (USP)?

2. **Market Potential** 📈
   - Does it solve a real, current/growing problem?
   - Quick view: target users, market size, key competitors, monetization model.

3. **Build Strategy** 🏗️
   - MVP → Beta → Scale: short 3-stage plan.
   - Ideal tech stack, architecture (e.g. monolith/microservices), and methodology (Agile, Lean).

4. **Cost & Team** 💰
   - Ballpark cost (dev, infra, tools), ideal team setup.
   - Cost-saving tips: OSS, no-code/low-code, outsourcing, phased rollouts.

5. **Improvements & Risks** ⚠️
   - UX/features to boost value.
   - Key risks (tech, market, legal), and how to reduce them.

Format your response with clear headers, bullet points, and actionable insights. Use emojis to make it visually appealing."""

    progress(0.3, desc="Connecting to AI model...")
    
    try:
        convo = model.start_chat(history=[
            {"role": "user", "parts": [system_prompt]}
        ])
        
        progress(0.6, desc="Analyzing your startup idea...")
        response = convo.send_message(prompt)
        
        progress(0.9, desc="Finalizing evaluation...")
        time.sleep(0.5)  
        progress(1.0, desc="Complete!")
        
        return response.text
        
    except Exception as e:
        return f"❌ **Error occurred:** {str(e)}\n\nPlease try again or check your API configuration."

def clear_inputs():
    """Clear all inputs"""
    return "", ""

def load_example(example_text):
    """Load example idea"""
    return example_text

examples = [
    "An AI-powered personal finance app that automatically categorizes expenses and provides investment recommendations based on spending patterns",
    "A platform connecting local farmers directly with restaurants, reducing food waste and supporting sustainable agriculture",
    "A VR-based remote collaboration tool specifically designed for creative teams working on 3D projects",
    "An app that uses machine learning to optimize home energy consumption by learning user behavior patterns"
]

custom_css = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}
.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.section-header {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
}
.example-box {
    background: #e3f2fd;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}
.example-box:hover {
    background: #bbdefb;
    transform: translateY(-2px);
}
"""

with gr.Blocks(css=custom_css, title="🚀Manthan The AI", theme=gr.themes.Soft()) as demo:
    
    
    gr.HTML("""
    <div class="main-header">
        <h1>🚀 Manthan The AI</h1>
        <p style="font-size: 1.2em; margin: 0;">Get expert analysis of your startup idea across 5 key pillars</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<div class="section-header"><h3>💡 Your Startup Idea</h3></div>')
            
            idea_input = gr.Textbox(
                label="Describe your startup idea",
                placeholder="e.g., An AI-powered app that helps people find the perfect pet based on their lifestyle, living situation, and preferences...",
                lines=6,
                max_lines=10,
                show_label=False
            )
            
            with gr.Row():
                evaluate_btn = gr.Button("🔍 Evaluate Idea", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", variant="secondary")
            
            gr.HTML('<div class="section-header"><h4>💭 Need inspiration? Try these examples:</h4></div>')
            
            for i, example in enumerate(examples):
                example_btn = gr.Button(
                    f"💡 Example {i+1}: {example[:80]}...",
                    variant="secondary",
                    size="sm"
                )
                example_btn.click(
                    fn=lambda x=example: x,
                    outputs=idea_input
                )
        
        with gr.Column(scale=2):
            gr.HTML('<div class="section-header"><h3>📊 Evaluation Results</h3></div>')
            
            output = gr.Textbox(
                label="Analysis",
                lines=25,
                max_lines=50,
                show_label=False,
                placeholder="Your detailed startup evaluation will appear here...\n\n✨ The analysis will cover:\n• Feasibility & Technical Requirements\n• Market Potential & Competition\n• Build Strategy & Development Plan\n• Cost Estimates & Team Structure\n• Risks & Improvement Suggestions",
                interactive=False
            )
            
            gr.HTML("""
            <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #ffc107;">
                <h4>💡 Tips for better results:</h4>
                <ul>
                    <li>Be specific about your target audience</li>
                    <li>Mention any unique features or technology</li>
                    <li>Include your business model if you have one in mind</li>
                    <li>Describe the problem you're solving clearly</li>
                </ul>
            </div>
            """)
    
    evaluate_btn.click(
        fn=evaluate_startup_idea,
        inputs=idea_input,
        outputs=output,
        show_progress=True
    )
    
    clear_btn.click(
        fn=clear_inputs,
        outputs=[idea_input, output]
    )
    
    gr.HTML("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #666; border-top: 1px solid #eee;">
        <p>🤖 Powered by Google's Gemini AI | Built with Gradio</p>
        <p style="font-size: 0.9em;">Get comprehensive startup evaluations in seconds</p>
    </div>
    """)

if __name__ == "__main__":
    demo.launch(
        share=True,
        show_error=True,
        server_name="0.0.0.0",  
        server_port=7860,
    #    enable_queue=True
    )