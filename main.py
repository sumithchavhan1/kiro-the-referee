#!/usr/bin/env python3
"""
Kiro The Referee - Week 6 Challenge
A comparison and trade-off analysis tool that helps users make informed choices.
Built with Kiro for accelerated AI-driven development.
"""

import json
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict

@dataclass
class Option:
    """Represents a single option for comparison."""
    name: str
    description: str
    pros: List[str]
    cons: List[str]
    cost: float
    performance: float  # 1-10 scale
    complexity: float  # 1-10 scale

class Referee:
    """The Referee - Compares options and explains trade-offs."""
    
    def __init__(self):
        self.options: List[Option] = []
        self.analysis_results: Dict = {}
    
    def add_option(self, option: Option) -> None:
        """Add an option to be compared."""
        self.options.append(option)
    
    def clear_options(self) -> None:
        """Clear all options."""
        self.options = []
    
    def compare_options(self) -> Dict:
        """Compare all added options and generate analysis."""
        if len(self.options) < 2:
            return {"error": "Please add at least 2 options for comparison"}
        
        comparison_results = {
            "total_options": len(self.options),
            "options": [asdict(opt) for opt in self.options],
            "analysis": self._generate_analysis(),
            "recommendation": self._generate_recommendation()
        }
        
        self.analysis_results = comparison_results
        return comparison_results
    
    def _generate_analysis(self) -> Dict:
        """Generate detailed analysis of trade-offs."""
        analysis = {}
        
        for i, option in enumerate(self.options):
            analysis[option.name] = {
                "cost_efficiency": round(option.performance / (option.cost + 0.01), 2),
                "complexity_score": option.complexity,
                "performance_score": option.performance,
                "pro_count": len(option.pros),
                "con_count": len(option.cons),
                "tradeoffs": self._analyze_tradeoffs(option)
            }
        
        return analysis
    
    def _analyze_tradeoffs(self, option: Option) -> Dict:
        """Analyze specific trade-offs for an option."""
        return {
            "cost_vs_performance": "High" if option.performance > 6 and option.cost > 500 else ("Balanced" if option.performance > 5 else "Low-cost"),
            "complexity_vs_benefit": "Complex but powerful" if option.complexity > 7 else ("Simple and effective" if option.complexity < 4 else "Moderate"),
            "overall_assessment": f"Cost-effective: {option.cost < 1000}, High performance: {option.performance > 7}, Low complexity: {option.complexity < 5}"
        }
    
    def _generate_recommendation(self) -> Dict:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Best for Cost
        cheapest = min(self.options, key=lambda x: x.cost)
        recommendations.append(f"Most cost-effective: {cheapest.name} at ${cheapest.cost}")
        
        # Best for Performance
        best_performance = max(self.options, key=lambda x: x.performance)
        recommendations.append(f"Best performance: {best_performance.name} with score {best_performance.performance}/10")
        
        # Easiest to use
        simplest = min(self.options, key=lambda x: x.complexity)
        recommendations.append(f"Easiest to use: {simplest.name} with complexity {simplest.complexity}/10")
        
        # Best overall value
        best_value = max(self.options, key=lambda x: (x.performance / (x.cost + 0.01)) - (x.complexity / 10))
        recommendations.append(f"Best overall value: {best_value.name}")
        
        return {"recommendations": recommendations}
    
    def print_comparison(self) -> None:
        """Print a formatted comparison report."""
        if not self.analysis_results:
            print("No analysis results available. Run compare_options() first.")
            return
        
        print("\n" + "="*60)
        print("KIRO THE REFEREE - COMPARISON ANALYSIS REPORT")
        print("="*60 + "\n")
        
        for option_data in self.analysis_results["options"]:
            print(f"\n{option_data['name']}")
            print("-" * 40)
            print(f"Description: {option_data['description']}")
            print(f"Cost: ${option_data['cost']}")
            print(f"Performance: {option_data['performance']}/10")
            print(f"Complexity: {option_data['complexity']}/10")
            print(f"Pros: {', '.join(option_data['pros'])}")
            print(f"Cons: {', '.join(option_data['cons'])}")
        
        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)
        
        for analysis in self.analysis_results["recommendation"]["recommendations"]:
            print(f"• {analysis}")

def main():
    """Main function demonstrating the Referee tool."""
    
    # Initialize referee
    referee = Referee()
    
    # Example: Compare Cloud Services
    aws = Option(
        name="AWS",
        description="Amazon Web Services - Industry leader in cloud computing",
        pros=["Extensive services", "Global infrastructure", "Strong ecosystem"],
        cons=["Complex pricing", "Steep learning curve", "Higher cost for beginners"],
        cost=1200,
        performance=9.5,
        complexity=8.0
    )
    
    gcp = Option(
        name="Google Cloud Platform",
        description="Google's cloud offering with strong ML capabilities",
        pros=["Excellent ML services", "Competitive pricing", "User-friendly"],
        cons=["Smaller ecosystem", "Less mature in some areas"],
        cost=950,
        performance=8.5,
        complexity=6.5
    )
    
    azure = Option(
        name="Microsoft Azure",
        description="Enterprise-focused cloud platform",
        pros=["Enterprise integration", "Strong support", "Good compliance"],
        cons=["Higher pricing", "Complex UI", "Vendor lock-in"],
        cost=1100,
        performance=8.0,
        complexity=7.5
    )
    
    # Add options
    referee.add_option(aws)
    referee.add_option(gcp)
    referee.add_option(azure)
    
    # Perform comparison
    results = referee.compare_options()
    
    # Print analysis
    referee.print_comparison()
    
    # Return results as JSON
    return json.dumps(results, indent=2)

if __name__ == "__main__":
    output = main()
    print("\n\nJSON Output:")
    print(output)
