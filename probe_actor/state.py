import pandas as pd


class FuzzerState:
    """Container for tracking scan results"""

    def __init__(self):
        self.errors = []
        self.refusals = []
        self.outputs = []

    def add_error(
        self,
        module_name: str,
        prompt: str,
        status_code: int | str,
        error_msg: str,
    ):
        """Add an error to the state"""
        self.errors.append((module_name, prompt, status_code, error_msg))

    def add_refusal(
        self, module_name: str, prompt: str, status_code: int, response_text: str
    ):
        """Add a refusal to the state"""
        self.refusals.append((module_name, prompt, status_code, response_text))

    def add_output(
        self, module_name: str, prompt: str, response_text: str, heuristic_refused: bool, controller_refused: bool | None,
    ):
        """Add an output to the state"""
        final_refused = heuristic_refused or (controller_refused if controller_refused is not None else False)
        
        self.outputs.append({
            "module": module_name,
            "prompt": prompt,
            "response": response_text,
            "heuristic_refused": heuristic_refused,
            "controller_refused": controller_refused,
            "final_refused": final_refused,
        })
        
        # if final_refused:
        #     self.refusals.append((module_name, prompt, 200, response_text))

    def get_last_output(self, prompt: str) -> str | None:
        """Get the last output for a given prompt"""
        for output in reversed(self.outputs):
            if output["prompt"] == prompt:
                return output["response"]
        return None

    def export_failures(self, filename: str = "failures.csv"):
        """Export failures to a CSV file"""
        # failure_data = self.errors + self.refusals
        # df = pd.DataFrame(
        #     failure_data, columns=["module", "prompt", "status_code", "content"]
        # )
        # df.to_csv(filename, index=False)
        
        df_errors = pd.DataFrame(
            self.errors,
            columns=["module", "prompt", "status_code", "content"],
        )
        
        df_refusals = pd.DataFrame(
            self.refusals,
            columns=["module", "prompt", "status_code", "content"],
        )
        
        df_outputs = pd.DataFrame(self.outputs)
        
        df_errors.to_csv("errors_" + filename, index=False)
        df_refusals.to_csv("refusals_" + filename, index=False)
        df_outputs.to_csv("outputs_" + filename, index=False)
