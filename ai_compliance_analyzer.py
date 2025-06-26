#!/usr/bin/env python3
"""
AI Compliance SEO Website Crawler and Analyzer
Analyzes websites for AI compliance factors in modern SEO (2025)
"""

import requests
import time
import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import defaultdict
import ssl
import socket
from datetime import datetime

class AIComplianceSEOAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.compliance_score = 0
        self.max_score = 100
        self.detailed_results = {}
        
    def analyze_website(self, url, max_pages=10):
        """Main analysis function that crawls and evaluates AI compliance"""
        print(f"🤖 Starting AI Compliance Analysis for: {url}")
        print("=" * 60)
        
        try:
            # Crawl the website
            pages_data = self.crawl_website(url, max_pages)
            
            # Analyze each compliance factor
            self.analyze_content_quality(pages_data)
            self.analyze_technical_performance(url, pages_data)
            self.analyze_semantic_structure(pages_data)
            self.analyze_ai_readiness(pages_data)
            self.analyze_eat_factors(pages_data)
            self.analyze_mobile_ai_optimization(url)
            
            # Generate final report
            return self.generate_compliance_report(url)
            
        except Exception as e:
            print(f"❌ Error analyzing website: {str(e)}")
            return None
    
    def crawl_website(self, base_url, max_pages):
        """Crawl website pages for analysis"""
        print(f"🕷️  Crawling website (max {max_pages} pages)...")
        
        pages_data = []
        visited = set()
        to_visit = [base_url]
        
        while to_visit and len(pages_data) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue
                
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    page_data = {
                        'url': url,
                        'soup': soup,
                        'response': response,
                        'content': response.text,
                        'status_code': response.status_code
                    }
                    pages_data.append(page_data)
                    visited.add(url)
                    
                    # Find internal links for further crawling
                    if len(pages_data) < max_pages:
                        links = soup.find_all('a', href=True)
                        for link in links[:5]:  # Limit to avoid infinite crawling
                            href = link.get('href')
                            if href:
                                full_url = urljoin(url, href)
                                if self.is_internal_link(base_url, full_url) and full_url not in visited:
                                    to_visit.append(full_url)
                    
                    print(f"✅ Analyzed: {url}")
                    time.sleep(1)  # Be respectful to the server
                    
            except Exception as e:
                print(f"⚠️  Failed to crawl {url}: {str(e)}")
                continue
        
        print(f"📊 Crawled {len(pages_data)} pages successfully")
        return pages_data
    
    def is_internal_link(self, base_url, link_url):
        """Check if a link is internal to the domain"""
        base_domain = urlparse(base_url).netloc
        link_domain = urlparse(link_url).netloc
        return base_domain == link_domain or link_domain == ''
    
    def analyze_content_quality(self, pages_data):
        """Analyze content quality for AI compliance"""
        print("\n📝 Analyzing Content Quality for AI Compliance...")
        
        quality_score = 0
        details = {
            'readability': 0,
            'semantic_richness': 0,
            'content_depth': 0,
            'keyword_optimization': 0
        }
        
        total_words = 0
        total_headings = 0
        total_paragraphs = 0
        
        for page in pages_data:
            soup = page['soup']
            text_content = soup.get_text()
            
            # Word count analysis
            words = len(text_content.split())
            total_words += words
            
            # Heading structure
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            total_headings += len(headings)
            
            # Paragraph count
            paragraphs = soup.find_all('p')
            total_paragraphs += len(paragraphs)
        
        avg_words = total_words / len(pages_data) if pages_data else 0
        
        # Content depth scoring
        if avg_words >= 1000:
            details['content_depth'] = 25
        elif avg_words >= 500:
            details['content_depth'] = 20
        elif avg_words >= 300:
            details['content_depth'] = 15
        else:
            details['content_depth'] = 10
        
        # Semantic richness (heading structure)
        if total_headings / len(pages_data) >= 5:
            details['semantic_richness'] = 20
        elif total_headings / len(pages_data) >= 3:
            details['semantic_richness'] = 15
        else:
            details['semantic_richness'] = 10
        
        # Readability approximation
        if total_paragraphs / len(pages_data) >= 5:
            details['readability'] = 15
        else:
            details['readability'] = 10
        
        quality_score = sum(details.values())
        self.compliance_score += quality_score
        self.detailed_results['content_quality'] = {
            'score': quality_score,
            'max_score': 80,
            'details': details,
            'avg_words_per_page': round(avg_words),
            'avg_headings_per_page': round(total_headings / len(pages_data), 1)
        }
        
        print(f"Content Quality Score: {quality_score}/80")
    
    def analyze_technical_performance(self, url, pages_data):
        """Analyze technical performance factors"""
        print("\n⚡ Analyzing Technical Performance...")
        
        tech_score = 0
        details = {
            'ssl_security': 0,
            'page_speed': 0,
            'mobile_friendly': 0,
            'clean_urls': 0
        }
        
        # SSL Check
        if url.startswith('https://'):
            details['ssl_security'] = 10
            print("✅ SSL Certificate detected")
        else:
            print("❌ No SSL Certificate")
        
        # Clean URLs check
        clean_url_count = 0
        # File extensions that are typically less SEO-friendly
        unfriendly_extensions = ['.php', '.html', '.htm', '.jsp', '.asp', '.aspx', '.cgi', '.pl', '.py', '.rb', '.do', '.action']

        for page in pages_data:
            url_path = urlparse(page['url']).path
            # Check for query parameters, ampersands, and unfriendly file extensions
            if (not re.search(r'[?&=]', url_path) and 
                not any(url_path.endswith(ext) for ext in unfriendly_extensions)):
                clean_url_count += 1
        
        if clean_url_count / len(pages_data) > 0.8:
            details['clean_urls'] = 10
        elif clean_url_count / len(pages_data) > 0.5:
            details['clean_urls'] = 7
        else:
            details['clean_urls'] = 3
        
        # Basic mobile-friendly check (viewport meta tag)
        mobile_friendly_count = 0
        for page in pages_data:
            viewport_tag = page['soup'].find('meta', attrs={'name': 'viewport'})
            if viewport_tag:
                mobile_friendly_count += 1
        
        if mobile_friendly_count / len(pages_data) > 0.8:
            details['mobile_friendly'] = 15
        elif mobile_friendly_count / len(pages_data) > 0.5:
            details['mobile_friendly'] = 10
        else:
            details['mobile_friendly'] = 5
        
        # Estimated page speed (based on response time)
        response_times = []
        for page in pages_data:
            if hasattr(page['response'], 'elapsed'):
                response_times.append(page['response'].elapsed.total_seconds())
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            if avg_response_time < 1.0:
                details['page_speed'] = 15
            elif avg_response_time < 2.0:
                details['page_speed'] = 10
            else:
                details['page_speed'] = 5
        
        tech_score = sum(details.values())
        self.compliance_score += tech_score
        self.detailed_results['technical_performance'] = {
            'score': tech_score,
            'max_score': 50,
            'details': details
        }
        
        print(f"Technical Performance Score: {tech_score}/50")
    
    def analyze_semantic_structure(self, pages_data):
        """Analyze semantic HTML structure for AI understanding"""
        print("\n🧠 Analyzing Semantic Structure...")
        
        semantic_score = 0
        details = {
            'structured_data': 0,
            'semantic_html': 0,
            'meta_optimization': 0
        }
        
        structured_data_count = 0
        semantic_html_count = 0
        meta_optimized_count = 0
        
        for page in pages_data:
            soup = page['soup']
            
            # Check for structured data (JSON-LD, Microdata, RDFa)
            json_ld = soup.find_all('script', {'type': 'application/ld+json'})
            microdata = soup.find_all(attrs={'itemtype': True})
            if json_ld or microdata:
                structured_data_count += 1
            
            # Check for semantic HTML5 elements
            semantic_elements = soup.find_all(['article', 'section', 'nav', 'header', 'footer', 'aside', 'main'])
            if len(semantic_elements) >= 3:
                semantic_html_count += 1
            
            # Check meta optimization
            title = soup.find('title')
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if title and meta_desc and len(title.text.strip()) > 10:
                meta_optimized_count += 1
        
        # Scoring
        if structured_data_count / len(pages_data) > 0.5:
            details['structured_data'] = 15
        elif structured_data_count > 0:
            details['structured_data'] = 10
        else:
            details['structured_data'] = 0
        
        if semantic_html_count / len(pages_data) > 0.7:
            details['semantic_html'] = 10
        elif semantic_html_count / len(pages_data) > 0.3:
            details['semantic_html'] = 7
        else:
            details['semantic_html'] = 3
        
        if meta_optimized_count / len(pages_data) > 0.8:
            details['meta_optimization'] = 10
        elif meta_optimized_count / len(pages_data) > 0.5:
            details['meta_optimization'] = 7
        else:
            details['meta_optimization'] = 3
        
        semantic_score = sum(details.values())
        self.compliance_score += semantic_score
        self.detailed_results['semantic_structure'] = {
            'score': semantic_score,
            'max_score': 35,
            'details': details,
            'structured_data_pages': structured_data_count,
            'semantic_html_pages': semantic_html_count
        }
        
        print(f"Semantic Structure Score: {semantic_score}/35")
    
    def analyze_ai_readiness(self, pages_data):
        """Analyze AI-specific readiness factors"""
        print("\n🤖 Analyzing AI Readiness...")
        
        ai_score = 0
        details = {
            'conversational_content': 0,
            'question_answering': 0,
            'contextual_clarity': 0
        }
        
        question_pages = 0
        conversational_pages = 0
        clear_context_pages = 0
        
        for page in pages_data:
            soup = page['soup']
            text_content = soup.get_text().lower()
            
            # Check for question-answer format
            if re.search(r'\b(what|how|why|when|where|who)\b.*\?', text_content):
                question_pages += 1
            
            # Check for conversational tone indicators
            conversational_indicators = ['you can', 'let\'s', 'here\'s how', 'follow these steps', 'you\'ll find']
            if any(indicator in text_content for indicator in conversational_indicators):
                conversational_pages += 1
            
            # Check for clear context (headers, subheaders, clear sections)
            headings = soup.find_all(['h1', 'h2', 'h3'])
            if len(headings) >= 3:
                clear_context_pages += 1
        
        # Scoring
        if question_pages / len(pages_data) > 0.3:
            details['question_answering'] = 10
        elif question_pages > 0:
            details['question_answering'] = 7
        
        if conversational_pages / len(pages_data) > 0.5:
            details['conversational_content'] = 10
        elif conversational_pages / len(pages_data) > 0.2:
            details['conversational_content'] = 7
        
        if clear_context_pages / len(pages_data) > 0.7:
            details['contextual_clarity'] = 10
        elif clear_context_pages / len(pages_data) > 0.4:
            details['contextual_clarity'] = 7
        
        ai_score = sum(details.values())
        self.compliance_score += ai_score
        self.detailed_results['ai_readiness'] = {
            'score': ai_score,
            'max_score': 30,
            'details': details
        }
        
        print(f"AI Readiness Score: {ai_score}/30")
    
    def analyze_eat_factors(self, pages_data):
        """Analyze E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)"""
        print("\n🏆 Analyzing E-E-A-T Factors...")
        
        eat_score = 0
        details = {
            'author_info': 0,
            'credibility_signals': 0,
            'content_freshness': 0
        }
        
        author_pages = 0
        credibility_pages = 0
        
        for page in pages_data:
            soup = page['soup']
            text_content = soup.get_text().lower()
            
            # Check for author information
            author_indicators = soup.find_all(attrs={'class': re.compile(r'author|byline|writer', re.I)})
            author_meta = soup.find_all('meta', attrs={'name': re.compile(r'author', re.I)})
            if author_indicators or author_meta:
                author_pages += 1
            
            # Check for credibility signals
            credibility_signals = ['about us', 'contact', 'privacy policy', 'terms', 'certification', 'accredited']
            if any(signal in text_content for signal in credibility_signals):
                credibility_pages += 1
        
        # Scoring
        if author_pages / len(pages_data) > 0.5:
            details['author_info'] = 7
        elif author_pages > 0:
            details['author_info'] = 4
        
        if credibility_pages / len(pages_data) > 0.3:
            details['credibility_signals'] = 8
        elif credibility_pages > 0:
            details['credibility_signals'] = 5
        
        # Content freshness (check for dates)
        date_pages = 0
        for page in pages_data:
            soup = page['soup']
            date_patterns = soup.find_all(attrs={'class': re.compile(r'date|time|published', re.I)})
            time_tags = soup.find_all('time')
            if date_patterns or time_tags:
                date_pages += 1
        
        if date_pages / len(pages_data) > 0.5:
            details['content_freshness'] = 5
        elif date_pages > 0:
            details['content_freshness'] = 3
        
        eat_score = sum(details.values())
        self.compliance_score += eat_score
        self.detailed_results['eat_factors'] = {
            'score': eat_score,
            'max_score': 20,
            'details': details
        }
        
        print(f"E-E-A-T Score: {eat_score}/20")
    
    def analyze_mobile_ai_optimization(self, url):
        """Analyze mobile and AI-specific optimization"""
        print("\n📱 Analyzing Mobile & AI Optimization...")
        
        mobile_score = 0
        details = {
            'responsive_design': 0,
            'core_web_vitals': 0
        }
        
        try:
            # Basic mobile optimization check
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check viewport meta tag
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if viewport and 'width=device-width' in viewport.get('content', ''):
                details['responsive_design'] = 10
                print("✅ Responsive design detected")
            
            # Estimate Core Web Vitals (basic approximation)
            if hasattr(response, 'elapsed') and response.elapsed.total_seconds() < 2:
                details['core_web_vitals'] = 5
                print("✅ Good response time detected")
            
        except Exception as e:
            print(f"⚠️  Mobile analysis error: {str(e)}")
        
        mobile_score = sum(details.values())
        self.compliance_score += mobile_score
        self.detailed_results['mobile_ai_optimization'] = {
            'score': mobile_score,
            'max_score': 15,
            'details': details
        }
        
        print(f"Mobile & AI Optimization Score: {mobile_score}/15")
    
    def generate_compliance_report(self, url):
        """Generate final AI compliance report"""
        print("\n" + "=" * 60)
        print("🤖 AI COMPLIANCE SEO REPORT")
        print("=" * 60)
        
        # Calculate percentage score
        percentage_score = (self.compliance_score / 250) * 100  # Total max score is 250
        
        # Determine compliance level
        if percentage_score >= 80:
            compliance_level = "🟢 EXCELLENT"
            recommendation = "Your website is highly AI-compliant!"
        elif percentage_score >= 60:
            compliance_level = "🟡 GOOD"
            recommendation = "Good compliance with room for improvement."
        elif percentage_score >= 40:
            compliance_level = "🟠 MODERATE"
            recommendation = "Moderate compliance - several areas need attention."
        else:
            compliance_level = "🔴 POOR"
            recommendation = "Poor compliance - significant improvements needed."
        
        report = {
            'url': url,
            'analysis_date': datetime.now().isoformat(),
            'overall_score': round(percentage_score, 1),
            'compliance_level': compliance_level,
            'recommendation': recommendation,
            'detailed_scores': self.detailed_results,
            'priority_actions': self.generate_priority_actions()
        }
        
        # Print summary
        print(f"🌐 Website: {url}")
        print(f"📊 Overall Score: {percentage_score:.1f}%")
        print(f"🎯 Compliance Level: {compliance_level}")
        print(f"💡 Recommendation: {recommendation}")
        
        print("\n📋 DETAILED BREAKDOWN:")
        for category, data in self.detailed_results.items():
            score = data['score']
            max_score = data['max_score']
            percentage = (score / max_score) * 100
            print(f"  • {category.replace('_', ' ').title()}: {score}/{max_score} ({percentage:.1f}%)")
        
        print("\n🚀 PRIORITY ACTIONS:")
        for i, action in enumerate(report['priority_actions'], 1):
            print(f"  {i}. {action}")
        
        print("\n" + "=" * 60)
        return report
    
    def generate_priority_actions(self):
        """Generate prioritized action items based on analysis"""
        actions = []
        
        # Check each category for improvement opportunities
        for category, data in self.detailed_results.items():
            score = data['score']
            max_score = data['max_score']
            percentage = (score / max_score) * 100
            
            if percentage < 50:  # Categories scoring below 50%
                if category == 'content_quality':
                    actions.append("Improve content depth and semantic richness with longer, well-structured articles")
                elif category == 'technical_performance':
                    actions.append("Optimize page speed, implement SSL, and ensure mobile-friendly design")
                elif category == 'semantic_structure':
                    actions.append("Add structured data markup and improve semantic HTML structure")
                elif category == 'ai_readiness':
                    actions.append("Create more conversational, question-answering content for AI engines")
                elif category == 'eat_factors':
                    actions.append("Add author information, credibility signals, and update content dates")
                elif category == 'mobile_ai_optimization':
                    actions.append("Improve mobile responsiveness and Core Web Vitals performance")
        
        if not actions:
            actions.append("Continue monitoring and maintaining current high standards")
            actions.append("Focus on creating fresh, expert content regularly")
        
        return actions[:5]  # Return top 5 priority actions

def main():
    """Main function to run the AI compliance analysis"""
    analyzer = AIComplianceSEOAnalyzer()
    
    # Get user input
    print("🤖 AI Compliance SEO Analyzer")
    print("=" * 40)
    url = input("Enter website URL to analyze: ").strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    max_pages = 5  # Default to 5 pages for demo purposes
    try:
        custom_pages = input(f"Number of pages to analyze (default {max_pages}): ").strip()
        if custom_pages:
            max_pages = int(custom_pages)
    except ValueError:
        print(f"Using default {max_pages} pages")
    
    # Run analysis
    report = analyzer.analyze_website(url, max_pages)
    
    if report:
        # Optionally save report to JSON file
        save_report = input("\nSave detailed report to JSON file? (y/n): ").strip().lower()
        if save_report == 'y':
            filename = f"ai_compliance_report_{urlparse(url).netloc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Report saved to: {filename}")
    
    print("\n✨ Analysis complete!")

if __name__ == "__main__":
    main()