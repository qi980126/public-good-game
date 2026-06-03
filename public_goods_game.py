"""
公共物品博弈游戏
Public Goods Game
"""

class PublicGoodsGame:
    def __init__(self, player1_name="玩家1", player2_name="玩家2"):
        self.player1_name = player1_name
        self.player2_name = player2_name

        # 初始代币
        self.initial_tokens = 100

        # 各轮系数
        self.multipliers = [1.3, 2.0, 3.0]

        # 游戏状态
        self.current_round = 0
        self.player1_tokens = self.initial_tokens
        self.player2_tokens = self.initial_tokens

        # 历史记录
        self.history = []

    def play_round(self, player1_contribution, player2_contribution):
        """
        进行一轮游戏

        Args:
            player1_contribution: 玩家1投入的代币数
            player2_contribution: 玩家2投入的代币数

        Returns:
            该轮的结果信息
        """
        # 验证输入
        if player1_contribution > self.player1_tokens:
            raise ValueError(f"{self.player1_name}投入金额超过当前持有代币")
        if player2_contribution > self.player2_tokens:
            raise ValueError(f"{self.player2_name}投入金额超过当前持有代币")
        if player1_contribution < 0 or player2_contribution < 0:
            raise ValueError("投入金额不能为负数")

        # 获取当前轮次的系数
        multiplier = self.multipliers[self.current_round]

        # 计算公共池
        public_pool = player1_contribution + player2_contribution

        # 计算乘以系数后的总金额
        total_after_multiplier = public_pool * multiplier

        # 平均分配
        each_share = total_after_multiplier / 2

        # 计算剩余代币
        player1_remaining = self.player1_tokens - player1_contribution
        player2_remaining = self.player2_tokens - player2_contribution

        # 计算最终金额
        player1_final = player1_remaining + each_share
        player2_final = player2_remaining + each_share

        # 更新玩家代币
        self.player1_tokens = player1_final
        self.player2_tokens = player2_final

        # 记录历史
        round_result = {
            'round': self.current_round + 1,
            'multiplier': multiplier,
            'player1_contribution': player1_contribution,
            'player2_contribution': player2_contribution,
            'public_pool': public_pool,
            'total_after_multiplier': total_after_multiplier,
            'each_share': each_share,
            'player1_final': player1_final,
            'player2_final': player2_final
        }
        self.history.append(round_result)

        # 进入下一轮
        self.current_round += 1

        return round_result

    def is_game_over(self):
        """检查游戏是否结束"""
        return self.current_round >= len(self.multipliers)

    def get_final_results(self):
        """获取最终结果"""
        if not self.is_game_over():
            return None

        return {
            'player1_name': self.player1_name,
            'player2_name': self.player2_name,
            'player1_final_tokens': self.player1_tokens,
            'player2_final_tokens': self.player2_tokens,
            'total_rounds': len(self.history),
            'history': self.history
        }


def print_round_result(result):
    """打印一轮结果"""
    print(f"\n{'='*60}")
    print(f"第 {result['round']} 轮 - 系数: {result['multiplier']}")
    print(f"{'='*60}")
    print(f"公共资源池总投入: {result['public_pool']} 代币")
    print(f"乘以系数后总金额: {result['total_after_multiplier']:.2f} 代币")
    print(f"每人分得: {result['each_share']:.2f} 代币")
    print(f"\n投入情况:")
    print(f"  玩家1投入: {result['player1_contribution']} 代币")
    print(f"  玩家2投入: {result['player2_contribution']} 代币")
    print(f"\n该轮结束后:")
    print(f"  玩家1持有: {result['player1_final']:.2f} 代币")
    print(f"  玩家2持有: {result['player2_final']:.2f} 代币")


def print_final_results(results):
    """打印最终结果"""
    print(f"\n{'='*60}")
    print(f"游戏结束！最终结果")
    print(f"{'='*60}")
    print(f"{results['player1_name']}: {results['player1_final_tokens']:.2f} 代币")
    print(f"{results['player2_name']}: {results['player2_final_tokens']:.2f} 代币")

    if results['player1_final_tokens'] > results['player2_final_tokens']:
        winner = results['player1_name']
    elif results['player2_final_tokens'] > results['player1_final_tokens']:
        winner = results['player2_name']
    else:
        winner = "平局"

    print(f"\n获胜者: {winner}")


def interactive_game():
    """交互式游戏"""
    print("欢迎来到公共物品博弈游戏！")
    print("="*60)
    print("游戏规则:")
    print("1. 两名玩家各拥有100代币")
    print("2. 共进行3轮，系数分别为: 1.3, 2.0, 3.0")
    print("3. 每轮玩家决定投入多少代币到公共资源池")
    print("4. 公共池总金额乘以系数后平均分配给两个玩家")
    print("5. 3轮结束后，代币最多的玩家获胜")
    print("="*60)

    # 创建游戏
    game = PublicGoodsGame()

    # 进行3轮游戏
    while not game.is_game_over():
        current_multiplier = game.multipliers[game.current_round]

        print(f"\n第 {game.current_round + 1} 轮 (系数: {current_multiplier})")
        print(f"玩家1当前持有: {game.player1_tokens:.2f} 代币")
        print(f"玩家2当前持有: {game.player2_tokens:.2f} 代币")

        # 获取玩家输入
        try:
            p1_input = float(input(f"\n玩家1投入多少代币? (0-{game.player1_tokens:.2f}): "))
            p2_input = float(input(f"玩家2投入多少代币? (0-{game.player2_tokens:.2f}): "))

            # 进行一轮游戏
            result = game.play_round(p1_input, p2_input)
            print_round_result(result)

        except ValueError as e:
            print(f"输入错误: {e}")
            continue

    # 显示最终结果
    final_results = game.get_final_results()
    print_final_results(final_results)


def simulation_game(player1_strategy, player2_strategy):
    """
    模拟游戏

    Args:
        player1_strategy: 玩家1的策略函数，接受当前轮数和代币数，返回投入金额
        player2_strategy: 玩家2的策略函数，接受当前轮数和代币数，返回投入金额
    """
    game = PublicGoodsGame("策略A", "策略B")

    print("公共物品博弈游戏模拟")
    print("="*60)

    while not game.is_game_over():
        current_round = game.current_round
        multiplier = game.multipliers[current_round]

        # 根据策略决定投入金额
        p1_contribution = player1_strategy(current_round, game.player1_tokens, multiplier)
        p2_contribution = player2_strategy(current_round, game.player2_tokens, multiplier)

        print(f"\n第 {current_round + 1} 轮 (系数: {multiplier})")
        print(f"{game.player1_name} 投入: {p1_contribution:.2f} 代币")
        print(f"{game.player2_name} 投入: {p2_contribution:.2f} 代币")

        # 进行一轮游戏
        result = game.play_round(p1_contribution, p2_contribution)
        print_round_result(result)

    # 显示最终结果
    final_results = game.get_final_results()
    print_final_results(final_results)


# 示例策略
def greedy_strategy(round_num, tokens, multiplier):
    """贪婪策略：投入0代币"""
    return 0

def cooperative_strategy(round_num, tokens, multiplier):
    """合作策略：投入所有代币"""
    return tokens

def balanced_strategy(round_num, tokens, multiplier):
    """平衡策略：投入一半代币"""
    return tokens / 2

def adaptive_strategy(round_num, tokens, multiplier):
    """自适应策略：根据系数调整投入"""
    if multiplier >= 2.0:
        return tokens * 0.8
    else:
        return tokens * 0.3


if __name__ == "__main__":
    # 运行交互式游戏
    interactive_game()

    # 或者运行模拟游戏
    # print("\n\n" + "="*60)
    # print("模拟游戏：贪婪策略 vs 合作策略")
    # print("="*60)
    # simulation_game(greedy_strategy, cooperative_strategy)

    # print("\n\n" + "="*60)
    # print("模拟游戏：平衡策略 vs 自适应策略")
    # print("="*60)
    # simulation_game(balanced_strategy, adaptive_strategy)