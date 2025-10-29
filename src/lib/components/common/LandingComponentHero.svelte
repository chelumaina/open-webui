<script lang="ts">
	import { onMount } from 'svelte';
	
	let isVisible = false;
	
	onMount(() => {
		isVisible = true;
	});
</script>

<div class="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
	<!-- Hero Section -->
    <section class="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-800 dark:via-purple-800 dark:to-pink-800">
		<!-- Animated background elements -->
		<div class="absolute inset-0 opacity-20">
			<div class="absolute top-20 left-10 w-72 h-72 bg-white rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
			<div class="absolute top-40 right-10 w-72 h-72 bg-yellow-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
			<div class="absolute -bottom-8 left-40 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-2000"></div>
		</div>
		
		<div class="relative container mx-auto px-4 py-24 md:py-32 text-center">
            <div class="transition-all duration-1000 transform {isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}">
				<h1 class="text-5xl md:text-7xl font-extrabold mb-6 text-white leading-tight">
					Intelligent Chat.<br/>
					<span class="bg-clip-text text-transparent bg-gradient-to-r from-yellow-200 to-pink-200">
						for Everyone in the Legal Field
					</span>
				</h1>
				<p class="text-xl md:text-2xl mb-10 max-w-3xl mx-auto text-gray-100 font-light">
					Enhanced AI-powered Chat with Gazette Notices, Laws/Legislations & Court decisions.
				</p>
				<p class="text-lg md:text-xl mb-10 max-w-3xl mx-auto text-gray-100 font-light">
					Empower your legal research and decision-making with our AI-driven chat platform. An AI legal research copilot that understands your jurisdiction. Ask in plain language, get grounded answers with paragraph-level citations to Gazette Notices, Acts (and subsidiary legislation), and authoritative case law—powered by secure RAG and optional firm-specific fine-tuning.
				<div class="flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
					<a href="/auth" class="group relative bg-white text-indigo-600 px-10 py-4 rounded-xl font-bold text-lg hover:bg-gray-50 transition-all duration-300 shadow-2xl hover:shadow-xl hover:scale-105 transform">
						<span class="relative z-10">Get Started Free</span>
						<div class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl opacity-0 group-hover:opacity-10 transition-opacity"></div>
					</a>
					<a href="#features" class="group bg-white/10 backdrop-blur-sm border-2 border-white/30 text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-white/20 transition-all duration-300 hover:scale-105 transform">
						Learn More
						<span class="inline-block ml-2 transform group-hover:translate-x-1 transition-transform">→</span>
					</a>
				</div>
			</div>
        </div>
		
		<!-- Wave separator -->
		<div class="absolute bottom-0 left-0 right-0">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" class="w-full h-auto">
				<path fill="currentColor" class="text-gray-50 dark:text-gray-900" d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,58.7C960,64,1056,64,1152,58.7C1248,53,1344,43,1392,37.3L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"></path>
			</svg>
		</div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 bg-gray-50 dark:bg-gray-900">
        <div class="container mx-auto px-4">
            <div class="text-center mb-16">
				<h2 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-4">
					Powerful Features for Smart AI Legal Research
				</h2>
				<p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
					Everything you need to make Smart and informed legal decisions
				</p>
			</div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">AI-Powered Conversational Legal Research</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Ask questions across Gazette Notices, statutes, regulations, and case law. Get concise answers with citations and confidence notes.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-pink-500 to-rose-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Legislation & Gazette Navigator</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Trace amendments, subsidiary legislation, and commencement dates. Compare versions and see change summaries.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Case Law Q&A</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Query holdings, ratio decidendi, and trends across courts. Pull precedent lists with one prompt and filter by year, court level, or topic.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Drafting Assistant</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Get help with legal drafting, including contracts, pleadings, and other documents. Improve your writing with AI suggestions.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Compliance & Checklists</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Create step-by-step procedures from statutory requirements; export as checklists with linked provisions.</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105 transform">
                    <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Knowledge Base & DMS Integration</h3>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed">Connect your document management system or knowledge repository to chat over internal materials, with strict access controls..</p>
                </div>
            </div>
        </div>
    </section>

    <!-- How It Works -->
    <section class="py-20 bg-white dark:bg-gray-800">
        <div class="container mx-auto px-4">
            <div class="text-center mb-16">
				<h2 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-4">
					How It Works
				</h2>
				<p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
					Get started in three simple steps
				</p>
			</div>
            
            <div class="relative">
				<!-- Connection line -->
				<div class="hidden md:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200 dark:from-indigo-900 dark:via-purple-900 dark:to-pink-900 transform -translate-y-1/2 z-0"></div>
				
				<div class="grid grid-cols-1 md:grid-cols-3 gap-12 relative z-10">
					<div class="text-center group">
						<div class="relative inline-block mb-6">
							<div class="w-32 h-32 bg-gradient-to-br from-indigo-500 to-purple-600 dark:from-indigo-600 dark:to-purple-700 rounded-3xl flex items-center justify-center mx-auto shadow-2xl group-hover:scale-110 transition-transform duration-300">
								<span class="text-white text-5xl font-extrabold">1</span>
							</div>
							<div class="absolute -top-2 -right-2 w-8 h-8 bg-yellow-400 rounded-full animate-ping"></div>
							<div class="absolute -top-2 -right-2 w-8 h-8 bg-yellow-400 rounded-full"></div>
						</div>
						<h3 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Create Your Account</h3>
						<p class="text-gray-600 dark:text-gray-400 leading-relaxed">Sign up in seconds and set up your investment preferences and watchlists.</p>
					</div>
					
					<div class="text-center group">
						<div class="relative inline-block mb-6">
							<div class="w-32 h-32 bg-gradient-to-br from-purple-500 to-pink-600 dark:from-purple-600 dark:to-pink-700 rounded-3xl flex items-center justify-center mx-auto shadow-2xl group-hover:scale-110 transition-transform duration-300">
								<span class="text-white text-5xl font-extrabold">2</span>
							</div>
							<div class="absolute -top-2 -right-2 w-8 h-8 bg-green-400 rounded-full animate-ping delay-500"></div>
							<div class="absolute -top-2 -right-2 w-8 h-8 bg-green-400 rounded-full"></div>
						</div>
						<h3 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Explore the Market</h3>
						<p class="text-gray-600 dark:text-gray-400 leading-relaxed">Analyze stocks with our advanced tools, AI forecasts, and sentiment analysis.</p>
					</div>
					
					<div class="text-center group">
						<div class="relative inline-block mb-6">
							<div class="w-32 h-32 bg-gradient-to-br from-pink-500 to-rose-600 dark:from-pink-600 dark:to-rose-700 rounded-3xl flex items-center justify-center mx-auto shadow-2xl group-hover:scale-110 transition-transform duration-300">
								<span class="text-white text-5xl font-extrabold">3</span>
							</div>
							<div class="absolute -top-2 -right-2 w-8 h-8 bg-blue-400 rounded-full animate-ping delay-1000"></div>
							<div class="absolute -top-2 -right-2 w-8 h-8 bg-blue-400 rounded-full"></div>
						</div>
						<h3 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Make Informed Decisions</h3>
						<p class="text-gray-600 dark:text-gray-400 leading-relaxed">Use our insights to build and manage your portfolio with confidence.</p>
					</div>
				</div>
			</div>
        </div>
    </section>

    <!-- Testimonials -->
    <section class="py-20 bg-gray-50 dark:bg-gray-900">
        <div class="container mx-auto px-4">
            <div class="text-center mb-16">
				<h2 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-4">
					What Our Users Say
				</h2>
				<p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
					Join thousands of satisfied investors
				</p>
			</div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:-translate-y-2 transform">
                    <div class="flex items-center mb-6">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4 shadow-lg">
							JD
						</div>
                        <div>
                            <h4 class="font-bold text-gray-900 dark:text-white">John Doe</h4>
                            <p class="text-sm text-gray-500 dark:text-gray-400">Active Investor</p>
                        </div>
                    </div>
					<div class="mb-4">
						<svg class="w-6 h-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
							<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
						</svg>
					</div>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed italic">"The AI forecasts have been incredibly accurate for my portfolio. I've seen a 23% return since using the platform's recommendations."</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:-translate-y-2 transform">
                    <div class="flex items-center mb-6">
                        <div class="w-14 h-14 bg-gradient-to-br from-pink-500 to-rose-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4 shadow-lg">
							JS
						</div>
                        <div>
                            <h4 class="font-bold text-gray-900 dark:text-white">Jane Smith</h4>
                            <p class="text-sm text-gray-500 dark:text-gray-400">Day Trader</p>
                        </div>
                    </div>
					<div class="mb-4">
						<svg class="w-6 h-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
							<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
						</svg>
					</div>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed italic">"The real-time alerts and sentiment analysis have completely transformed my trading strategy. I'm making better decisions faster."</p>
                </div>
                
                <div class="group bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:-translate-y-2 transform">
                    <div class="flex items-center mb-6">
                        <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4 shadow-lg">
							RJ
						</div>
                        <div>
                            <h4 class="font-bold text-gray-900 dark:text-white">Robert Johnson</h4>
                            <p class="text-sm text-gray-500 dark:text-gray-400">Long-term Investor</p>
                        </div>
                    </div>
					<div class="mb-4">
						<svg class="w-6 h-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
							<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
						</svg>
					</div>
                    <p class="text-gray-600 dark:text-gray-400 leading-relaxed italic">"The portfolio insights and rebalancing suggestions have helped me optimize my holdings and reduce risk significantly."</p>
                </div>
            </div>
        </div>
    </section>

	<!-- CTA Section -->
	<section class="py-20 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-800 dark:via-purple-800 dark:to-pink-800 relative overflow-hidden">
		<div class="absolute inset-0 opacity-10">
			<div class="absolute top-0 left-1/4 w-96 h-96 bg-white rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
			<div class="absolute bottom-0 right-1/4 w-96 h-96 bg-yellow-200 rounded-full mix-blend-multiply filter blur-3xl animate-pulse delay-1000"></div>
		</div>
		
		<div class="container mx-auto px-4 text-center relative z-10">
			<h2 class="text-4xl md:text-5xl font-extrabold text-white mb-6">
				Ready to Start Your Investment Journey?
			</h2>
			<p class="text-xl text-gray-100 mb-10 max-w-2xl mx-auto">
				Join thousands of investors who trust our platform for smarter trading decisions.
			</p>
			<a href="#" class="inline-block bg-white text-indigo-600 px-12 py-5 rounded-xl font-bold text-lg hover:bg-gray-50 transition-all duration-300 shadow-2xl hover:shadow-xl hover:scale-105 transform">
				Get Started Today - It's Free
			</a>
			<p class="text-sm text-gray-200 mt-6">No credit card required • Cancel anytime</p>
		</div>
	</section>

   
</div>

<style>
	@keyframes pulse {
		0%, 100% {
			opacity: 0.6;
		}
		50% {
			opacity: 1;
		}
	}
	
	.delay-500 {
		animation-delay: 500ms;
	}
	
	.delay-1000 {
		animation-delay: 1000ms;
	}
	
	.delay-2000 {
		animation-delay: 2000ms;
	}
</style>
