import radon.complexity as radon_cc
import radon.raw as radon_raw
import radon.metrics as radon_metrics
import lizard
import os

class FeatureExtractor:
    def extract_from_code(self, code_content, filename="temp.py"):
        """Extracts software metrics from code using Radon (Python) or Lizard (Others)."""
        try:
            # Determine language based on extension
            _, ext = os.path.splitext(filename)
            is_python = ext.lower() == '.py' or filename == "pasted_code.py" # Default pasted to Python if not specified, but we might want to detect? 
            # Actually, for pasted code, we might not know the extension. 
            # But let's assume if it's explicitly .py or default, we try radon first.
            # If radon fails or it's not python, we use lizard.
            
            if is_python:
                try:
                    return self._extract_python_radon(code_content)
                except Exception:
                    # Fallback to lizard if radon fails (e.g. syntax error or not actually python)
                    return self._extract_lizard(code_content, filename)
            else:
                return self._extract_lizard(code_content, filename)

        except Exception as e:
            print(f"Error extracting features: {e}")
            return None

    def _extract_python_radon(self, code_content):
        # Cyclomatic Complexity
        cc = radon_cc.cc_visit(code_content)
        avg_cc = sum([x.complexity for x in cc]) / len(cc) if cc else 0
        
        # Raw Metrics (LOC, SLOC, Comments)
        raw = radon_raw.analyze(code_content)
        
        # Halstead Metrics
        hal = radon_metrics.h_visit(code_content)
        hal_volume = hal.total.volume if hal else 0
        
        return {
            'loc': raw.loc,
            'sloc': raw.sloc,
            'cyclomatic_complexity': avg_cc,
            'halstead_volume': hal_volume
        }

    def _extract_lizard(self, code_content, filename):
        # Write to temp file because lizard analysis usually works on files or strings
        # lizard.analyze_file.analyze_source_code(filename, code_content)
        
        analysis = lizard.analyze_file.analyze_source_code(filename, code_content)
        
        # Lizard returns a FileInfo object
        # nloc: Lines of code without comments
        # CCN: Cyclomatic Complexity Number
        
        if not analysis:
            return None

        # Calculate average CCN
        total_cc = sum(func.cyclomatic_complexity for func in analysis.function_list)
        avg_cc = total_cc / len(analysis.function_list) if analysis.function_list else 0
        
        # If no functions found, lizard might still give nloc
        # But for complexity, if no functions, it's basically 1 or 0? Let's say 1.
        if not analysis.function_list and analysis.nloc > 0:
             avg_cc = 1

        return {
            'loc': analysis.nloc, # Lizard nloc is basically SLOC
            'sloc': analysis.nloc,
            'cyclomatic_complexity': avg_cc,
            'halstead_volume': 0 # Lizard doesn't provide Halstead
        }
